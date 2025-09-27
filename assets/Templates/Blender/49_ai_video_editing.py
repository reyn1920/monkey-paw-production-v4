"""AI Video Editing Module

Provides comprehensive AI-powered video editing capabilities including
automated editing, scene detection, transitions, and effects.
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from dataclasses import dataclass
import json
import subprocess
import tempfile
import os

# Video processing imports (would be installed via pip)
try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


class VideoEditType(Enum):
    """Types of video editing operations"""

    CUT = "cut"
    TRIM = "trim"
    MERGE = "merge"
    TRANSITION = "transition"
    EFFECT = "effect"
    COLOR_CORRECTION = "color_correction"
    AUDIO_SYNC = "audio_sync"
    STABILIZATION = "stabilization"
    SPEED_CHANGE = "speed_change"
    OVERLAY = "overlay"


class TransitionType(Enum):
    """Types of video transitions"""

    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    CROSSFADE = "crossfade"
    WIPE = "wipe"
    SLIDE = "slide"
    ZOOM = "zoom"
    DISSOLVE = "dissolve"
    CUT = "cut"


class EffectType(Enum):
    """Types of video effects"""

    BLUR = "blur"
    SHARPEN = "sharpen"
    BRIGHTNESS = "brightness"
    CONTRAST = "contrast"
    SATURATION = "saturation"
    HUE_SHIFT = "hue_shift"
    VINTAGE = "vintage"
    BLACK_WHITE = "black_white"
    SEPIA = "sepia"
    VIGNETTE = "vignette"


@dataclass
class VideoClip:
    """Represents a video clip with metadata"""

    file_path: str
    start_time: float = 0.0
    end_time: Optional[float] = None
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    format: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class EditOperation:
    """Represents a video editing operation"""

    operation_type: VideoEditType
    parameters: dict[str, Any]
    target_clip: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    priority: int = 0


@dataclass
class EditResult:
    """Result of a video editing operation"""

    success: bool
    output_path: Optional[str] = None
    duration: Optional[float] = None
    file_size: Optional[int] = None
    processing_time: Optional[float] = None
    error: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SceneDetector:
    """Detects scenes and cuts in video content"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.threshold = 0.3  # Scene change threshold

    async def detect_scenes(self, video_path: str) -> list[tuple[float, float]]:
        """Detect scene boundaries in video"""
        try:
            if not cv2:
                # Fallback to basic time-based scenes
                return await self._detect_time_based_scenes(video_path)

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Cannot open video: {video_path}")

            scenes = []
            prev_frame = None
            frame_count = 0
            fps = cap.get(cv2.CAP_PROP_FPS)
            scene_start = 0.0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if prev_frame is not None and cv2 is not None and np is not None:
                    # Calculate frame difference
                    diff = cv2.absdiff(prev_frame, frame)
                    diff_score = np.mean(diff) / 255.0

                    if diff_score > self.threshold:
                        # Scene change detected
                        scene_end = frame_count / fps
                        scenes.append((scene_start, scene_end))
                        scene_start = scene_end

                prev_frame = frame.copy()
                frame_count += 1

            # Add final scene
            if scene_start < frame_count / fps:
                scenes.append((scene_start, frame_count / fps))

            cap.release()
            return scenes

        except Exception as e:
            self.logger.error(f"Scene detection failed: {e}")
            return await self._detect_time_based_scenes(video_path)

    async def _detect_time_based_scenes(
        self, video_path: str
    ) -> list[tuple[float, float]]:
        """Fallback scene detection based on time intervals"""
        try:
            # Get video duration using ffprobe
            cmd = [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                video_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                info = json.loads(result.stdout)
                duration = float(info["format"]["duration"])

                # Create 10-second scenes
                scenes = []
                scene_length = 10.0
                current_time = 0.0

                while current_time < duration:
                    end_time = min(current_time + scene_length, duration)
                    scenes.append((current_time, end_time))
                    current_time = end_time

                return scenes

            return [(0.0, 60.0)]  # Default single scene

        except Exception as e:
            self.logger.error(f"Time-based scene detection failed: {e}")
            return [(0.0, 60.0)]


class VideoProcessor:
    """Core video processing functionality"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = tempfile.mkdtemp(prefix="video_edit_")

    async def get_video_info(self, video_path: str) -> dict[str, Any]:
        """Get comprehensive video information"""
        try:
            cmd = [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                video_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                return json.loads(result.stdout)

            return {"error": "Failed to get video info"}

        except Exception as e:
            self.logger.error(f"Failed to get video info: {e}")
            return {"error": str(e)}

    async def trim_video(
        self, input_path: str, start_time: float, end_time: float, output_path: str
    ) -> EditResult:
        """Trim video to specified time range"""
        try:
            duration = end_time - start_time

            cmd = [
                "ffmpeg",
                "-i",
                input_path,
                "-ss",
                str(start_time),
                "-t",
                str(duration),
                "-c",
                "copy",
                "-avoid_negative_ts",
                "make_zero",
                output_path,
                "-y",
            ]

            start_process_time = datetime.now()
            result = subprocess.run(cmd, capture_output=True, text=True)
            processing_time = (datetime.now() - start_process_time).total_seconds()

            if result.returncode == 0:
                file_size = (
                    os.path.getsize(output_path) if os.path.exists(output_path) else 0
                )

                return EditResult(
                    success=True,
                    output_path=output_path,
                    duration=duration,
                    file_size=file_size,
                    processing_time=processing_time,
                )

            return EditResult(
                success=False,
                error=f"FFmpeg error: {result.stderr}",
                processing_time=processing_time,
            )

        except Exception as e:
            self.logger.error(f"Video trimming failed: {e}")
            return EditResult(success=False, error=str(e))

    async def merge_videos(
        self, video_paths: list[str], output_path: str
    ) -> EditResult:
        """Merge multiple videos into one"""
        list_file = None
        try:
            # Create temporary file list for ffmpeg
            list_file = os.path.join(self.temp_dir, "merge_list.txt")

            with open(list_file, "w") as f:
                for path in video_paths:
                    f.write(f"file '{path}'\n")

            cmd = [
                "ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_file,
                "-c",
                "copy",
                output_path,
                "-y",
            ]

            start_time = datetime.now()
            result = subprocess.run(cmd, capture_output=True, text=True)
            processing_time = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                file_size = (
                    os.path.getsize(output_path) if os.path.exists(output_path) else 0
                )

                return EditResult(
                    success=True,
                    output_path=output_path,
                    file_size=file_size,
                    processing_time=processing_time,
                )

            return EditResult(
                success=False,
                error=f"Video merge failed: {result.stderr}",
                processing_time=processing_time,
            )

        except Exception as e:
            self.logger.error(f"Video merging failed: {e}")
            return EditResult(success=False, error=str(e))
        finally:
            # Clean up temp file
            if list_file and os.path.exists(list_file):
                os.remove(list_file)

    async def apply_transition(
        self,
        clip1_path: str,
        clip2_path: str,
        transition_type: TransitionType,
        duration: float,
        output_path: str,
    ) -> EditResult:
        """Apply transition between two video clips"""
        try:
            if transition_type == TransitionType.CROSSFADE:
                # Crossfade transition using ffmpeg
                cmd = [
                    "ffmpeg",
                    "-i",
                    clip1_path,
                    "-i",
                    clip2_path,
                    "-filter_complex",
                    f"[0][1]xfade=transition=fade:duration={duration}:offset=0",
                    output_path,
                    "-y",
                ]
            elif transition_type == TransitionType.FADE_OUT:
                # Fade out effect
                cmd = [
                    "ffmpeg",
                    "-i",
                    clip1_path,
                    "-vf",
                    f"fade=out:st=0:d={duration}",
                    output_path,
                    "-y",
                ]
            else:
                # Default to simple concatenation
                return await self.merge_videos([clip1_path, clip2_path], output_path)

            start_time = datetime.now()
            result = subprocess.run(cmd, capture_output=True, text=True)
            processing_time = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                file_size = (
                    os.path.getsize(output_path) if os.path.exists(output_path) else 0
                )

                return EditResult(
                    success=True,
                    output_path=output_path,
                    file_size=file_size,
                    processing_time=processing_time,
                )

            return EditResult(
                success=False,
                error=f"Transition failed: {result.stderr}",
                processing_time=processing_time,
            )

        except Exception as e:
            self.logger.error(f"Transition application failed: {e}")
            return EditResult(success=False, error=str(e))


class EffectsProcessor:
    """Handles video effects and filters"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def apply_effect(
        self,
        input_path: str,
        effect_type: EffectType,
        parameters: dict[str, Any],
        output_path: str,
    ) -> EditResult:
        """Apply visual effect to video"""
        try:
            filter_string = self._build_filter_string(effect_type, parameters)

            cmd = [
                "ffmpeg",
                "-i",
                input_path,
                "-vf",
                filter_string,
                "-c:a",
                "copy",
                output_path,
                "-y",
            ]

            start_time = datetime.now()
            result = subprocess.run(cmd, capture_output=True, text=True)
            processing_time = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                file_size = (
                    os.path.getsize(output_path) if os.path.exists(output_path) else 0
                )

                return EditResult(
                    success=True,
                    output_path=output_path,
                    file_size=file_size,
                    processing_time=processing_time,
                    metadata={"effect": effect_type.value, "parameters": parameters},
                )

            return EditResult(
                success=False,
                error=f"Effect application failed: {result.stderr}",
                processing_time=processing_time,
            )

        except Exception as e:
            self.logger.error(f"Effect processing failed: {e}")
            return EditResult(success=False, error=str(e))

    def _build_filter_string(
        self, effect_type: EffectType, parameters: dict[str, Any]
    ) -> str:
        """Build FFmpeg filter string for effect"""
        if effect_type == EffectType.BLUR:
            radius = parameters.get("radius", 5)
            return f"boxblur={radius}:{radius}"

        elif effect_type == EffectType.BRIGHTNESS:
            value = parameters.get("value", 0.1)
            return f"eq=brightness={value}"

        elif effect_type == EffectType.CONTRAST:
            value = parameters.get("value", 1.2)
            return f"eq=contrast={value}"

        elif effect_type == EffectType.SATURATION:
            value = parameters.get("value", 1.5)
            return f"eq=saturation={value}"

        elif effect_type == EffectType.BLACK_WHITE:
            return "hue=s=0"

        elif effect_type == EffectType.SEPIA:
            return "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131"

        elif effect_type == EffectType.VIGNETTE:
            return "vignette=PI/4"

        else:
            return "null"  # No effect


class AIVideoEditor:
    """Main AI-powered video editing class"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scene_detector = SceneDetector()
        self.video_processor = VideoProcessor()
        self.effects_processor = EffectsProcessor()
        self.temp_dir = tempfile.mkdtemp(prefix="ai_video_editor_")

    async def analyze_video(self, video_path: str) -> dict[str, Any]:
        """Comprehensive video analysis"""
        try:
            # Get basic video info
            video_info = await self.video_processor.get_video_info(video_path)

            # Detect scenes
            scenes = await self.scene_detector.detect_scenes(video_path)

            # Extract key metrics
            analysis = {
                "file_path": video_path,
                "video_info": video_info,
                "scenes": scenes,
                "scene_count": len(scenes),
                "total_duration": sum(end - start for start, end in scenes),
                "analysis_timestamp": datetime.now().isoformat(),
            }

            return analysis

        except Exception as e:
            self.logger.error(f"Video analysis failed: {e}")
            return {"error": str(e)}

    async def auto_edit_video(
        self, video_path: str, style: str = "dynamic"
    ) -> EditResult:
        """Automatically edit video based on AI analysis"""
        try:
            # Analyze video first
            analysis = await self.analyze_video(video_path)

            if "error" in analysis:
                return EditResult(success=False, error=analysis["error"])

            scenes = analysis["scenes"]

            # Generate edit plan based on style
            edit_operations = self._generate_edit_plan(scenes, style)

            # Execute edit operations
            output_path = os.path.join(
                self.temp_dir,
                f"auto_edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
            )

            result = await self._execute_edit_plan(
                video_path, edit_operations, output_path
            )

            return result

        except Exception as e:
            self.logger.error(f"Auto video editing failed: {e}")
            return EditResult(success=False, error=str(e))

    def _generate_edit_plan(
        self, scenes: list[tuple[float, float]], style: str
    ) -> list[EditOperation]:
        """Generate editing plan based on scenes and style"""
        operations = []

        if style == "dynamic":
            # Keep shorter, more dynamic scenes
            for i, (start, end) in enumerate(scenes):
                duration = end - start

                if duration > 5.0:  # Trim long scenes
                    new_duration = min(duration * 0.7, 8.0)
                    operations.append(
                        EditOperation(
                            operation_type=VideoEditType.TRIM,
                            parameters={"start": start, "duration": new_duration},
                            priority=1,
                        )
                    )

                # Add transition between scenes
                if i < len(scenes) - 1:
                    operations.append(
                        EditOperation(
                            operation_type=VideoEditType.TRANSITION,
                            parameters={
                                "type": TransitionType.CROSSFADE,
                                "duration": 0.5,
                            },
                            priority=2,
                        )
                    )

        elif style == "cinematic":
            # Add cinematic effects
            for start, end in scenes:
                operations.append(
                    EditOperation(
                        operation_type=VideoEditType.EFFECT,
                        parameters={"effect": EffectType.CONTRAST, "value": 1.2},
                        priority=1,
                    )
                )

        return operations

    async def _execute_edit_plan(
        self, input_path: str, operations: list[EditOperation], output_path: str
    ) -> EditResult:
        """Execute the generated edit plan"""
        try:
            current_path = input_path
            temp_files = []

            # Sort operations by priority
            operations.sort(key=lambda x: x.priority)

            for i, operation in enumerate(operations):
                temp_output = os.path.join(self.temp_dir, f"temp_{i}.mp4")
                temp_files.append(temp_output)

                if operation.operation_type == VideoEditType.TRIM:
                    params = operation.parameters
                    result = await self.video_processor.trim_video(
                        current_path,
                        params["start"],
                        params["start"] + params["duration"],
                        temp_output,
                    )

                elif operation.operation_type == VideoEditType.EFFECT:
                    params = operation.parameters
                    result = await self.effects_processor.apply_effect(
                        current_path,
                        params["effect"],
                        {"value": params.get("value", 1.0)},
                        temp_output,
                    )

                else:
                    # Skip unsupported operations
                    continue

                if not result.success:
                    return result

                current_path = temp_output

            # Copy final result to output path
            if current_path != input_path:
                import shutil

                shutil.copy2(current_path, output_path)
            else:
                # No operations were applied, copy original
                import shutil

                shutil.copy2(input_path, output_path)

            # Clean up temp files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

            file_size = (
                os.path.getsize(output_path) if os.path.exists(output_path) else 0
            )

            return EditResult(
                success=True,
                output_path=output_path,
                file_size=file_size,
                metadata={"operations_applied": len(operations)},
            )

        except Exception as e:
            self.logger.error(f"Edit plan execution failed: {e}")
            return EditResult(success=False, error=str(e))

    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil

            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")


# Convenience functions


async def edit_video_auto(video_path: str, style: str = "dynamic") -> EditResult:
    """Convenience function for automatic video editing"""
    editor = AIVideoEditor()
    try:
        return await editor.auto_edit_video(video_path, style)
    finally:
        editor.cleanup()


async def trim_video_clip(
    input_path: str, start_time: float, end_time: float, output_path: str
) -> EditResult:
    """Convenience function for video trimming"""
    processor = VideoProcessor()
    return await processor.trim_video(input_path, start_time, end_time, output_path)


async def merge_video_clips(video_paths: list[str], output_path: str) -> EditResult:
    """Convenience function for video merging"""
    processor = VideoProcessor()
    return await processor.merge_videos(video_paths, output_path)


async def apply_video_effect(
    input_path: str,
    effect_type: EffectType,
    parameters: dict[str, Any],
    output_path: str,
) -> EditResult:
    """Convenience function for applying video effects"""
    effects = EffectsProcessor()
    return await effects.apply_effect(input_path, effect_type, parameters, output_path)
