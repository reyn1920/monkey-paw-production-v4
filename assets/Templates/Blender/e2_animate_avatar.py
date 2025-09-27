"""Avatar Animation Module - Advanced avatar animation and rigging system"""

import os
import logging
from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import tempfile
import json
import math

# Optional imports with fallbacks
try:
    import numpy as np
except ImportError:
    np = None

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    Image = None
    ImageDraw = None
    ImageFilter = None

try:
    import cv2
except ImportError:
    cv2 = None


class AnimationType(Enum):
    """Types of avatar animations"""

    IDLE = "idle"
    TALKING = "talking"
    GESTURING = "gesturing"
    WALKING = "walking"
    DANCING = "dancing"
    EMOTIONAL = "emotional"
    CUSTOM = "custom"


class EmotionType(Enum):
    """Emotion types for avatar expressions"""

    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    CONFUSED = "confused"
    EXCITED = "excited"
    THOUGHTFUL = "thoughtful"


class RigType(Enum):
    """Avatar rig types"""

    BASIC_2D = "basic_2d"
    ADVANCED_2D = "advanced_2d"
    SIMPLE_3D = "simple_3d"
    FULL_3D = "full_3d"
    MOCAP_READY = "mocap_ready"


class QualityLevel(Enum):
    """Animation quality levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"


@dataclass
class AnimationKeyframe:
    """Single keyframe in animation"""

    timestamp: float
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    scale: tuple[float, float, float] = (1.0, 1.0, 1.0)
    blend_shape_weights: Optional[dict[str, float]] = None
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.blend_shape_weights is None:
            self.blend_shape_weights = {}
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AnimationSequence:
    """Complete animation sequence"""

    name: str
    animation_type: AnimationType
    keyframes: list[AnimationKeyframe]
    duration: float
    fps: int = 30
    loop: bool = False
    emotion: EmotionType = EmotionType.NEUTRAL
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AvatarRig:
    """Avatar rig definition"""

    name: str
    rig_type: RigType
    bones: list[str]
    blend_shapes: list[str]
    constraints: Optional[dict[str, Any]] = None
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.constraints is None:
            self.constraints = {}
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AnimationRequest:
    """Request for avatar animation"""

    avatar_path: str
    animation_type: AnimationType
    duration: float
    output_path: Optional[str] = None
    emotion: EmotionType = EmotionType.NEUTRAL
    quality: QualityLevel = QualityLevel.MEDIUM
    fps: int = 30
    loop: bool = False
    custom_parameters: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.custom_parameters is None:
            self.custom_parameters = {}


@dataclass
class AnimationResult:
    """Result of avatar animation"""

    success: bool
    output_path: Optional[str] = None
    duration: Optional[float] = None
    frame_count: Optional[int] = None
    processing_time: Optional[float] = None
    animation_type: Optional[AnimationType] = None
    quality_score: Optional[float] = None
    error: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BlendShapeController:
    """Controls facial blend shapes for expressions"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.emotion_mappings = self._initialize_emotion_mappings()

    def _initialize_emotion_mappings(self) -> dict[EmotionType, dict[str, float]]:
        """Initialize emotion to blend shape mappings"""
        return {
            EmotionType.NEUTRAL: {
                "eyebrow_raise": 0.0,
                "eye_squint": 0.0,
                "mouth_smile": 0.0,
                "mouth_frown": 0.0,
                "jaw_open": 0.0,
            },
            EmotionType.HAPPY: {
                "eyebrow_raise": 0.2,
                "eye_squint": 0.3,
                "mouth_smile": 0.8,
                "mouth_frown": 0.0,
                "jaw_open": 0.1,
            },
            EmotionType.SAD: {
                "eyebrow_raise": 0.0,
                "eye_squint": 0.1,
                "mouth_smile": 0.0,
                "mouth_frown": 0.7,
                "jaw_open": 0.0,
            },
            EmotionType.ANGRY: {
                "eyebrow_raise": -0.3,
                "eye_squint": 0.6,
                "mouth_smile": 0.0,
                "mouth_frown": 0.4,
                "jaw_open": 0.2,
            },
            EmotionType.SURPRISED: {
                "eyebrow_raise": 0.8,
                "eye_squint": -0.2,
                "mouth_smile": 0.0,
                "mouth_frown": 0.0,
                "jaw_open": 0.6,
            },
            EmotionType.CONFUSED: {
                "eyebrow_raise": 0.3,
                "eye_squint": 0.2,
                "mouth_smile": 0.0,
                "mouth_frown": 0.1,
                "jaw_open": 0.1,
            },
        }

    def get_emotion_weights(
        self, emotion: EmotionType, intensity: float = 1.0
    ) -> dict[str, float]:
        """Get blend shape weights for emotion"""
        base_weights = self.emotion_mappings.get(
            emotion, self.emotion_mappings[EmotionType.NEUTRAL]
        )
        return {key: value * intensity for key, value in base_weights.items()}

    def interpolate_emotions(
        self, emotion1: EmotionType, emotion2: EmotionType, blend_factor: float
    ) -> dict[str, float]:
        """Interpolate between two emotions"""
        weights1 = self.get_emotion_weights(emotion1)
        weights2 = self.get_emotion_weights(emotion2)

        result = {}
        all_keys = set(weights1.keys()) | set(weights2.keys())

        for key in all_keys:
            val1 = weights1.get(key, 0.0)
            val2 = weights2.get(key, 0.0)
            result[key] = val1 * (1.0 - blend_factor) + val2 * blend_factor

        return result


class MotionGenerator:
    """Generates motion patterns for avatars"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_idle_motion(
        self, duration: float, fps: int = 30
    ) -> list[AnimationKeyframe]:
        """Generate subtle idle motion"""
        keyframes = []
        frame_count = int(duration * fps)

        for i in range(frame_count):
            timestamp = i / fps

            # Subtle breathing motion
            breath_cycle = math.sin(timestamp * 2 * math.pi * 0.2)  # 0.2 Hz breathing
            chest_y = breath_cycle * 0.01

            # Slight head movement
            head_sway = math.sin(timestamp * 2 * math.pi * 0.1) * 0.005

            keyframe = AnimationKeyframe(
                timestamp=timestamp,
                position=(0.0, chest_y, 0.0),
                rotation=(head_sway, 0.0, 0.0),
            )
            keyframes.append(keyframe)

        return keyframes

    def generate_talking_motion(
        self, duration: float, fps: int = 30, speech_intensity: float = 1.0
    ) -> list[AnimationKeyframe]:
        """Generate talking motion with lip sync approximation"""
        keyframes = []
        frame_count = int(duration * fps)

        for i in range(frame_count):
            timestamp = i / fps

            # Simulate speech patterns
            # Variable speech frequency
            speech_freq = 4.0 + (speech_intensity * 2.0)
            jaw_open = (
                abs(math.sin(timestamp * 2 * math.pi * speech_freq))
                * speech_intensity
                * 0.3
            )

            # Head movement during speech
            head_nod = math.sin(timestamp * 2 * math.pi * 0.5) * 0.02

            # Blend shapes for speech
            blend_shapes = {
                "jaw_open": jaw_open,
                "mouth_smile": 0.1 * speech_intensity,
                "eyebrow_raise": 0.05 * speech_intensity,
            }

            keyframe = AnimationKeyframe(
                timestamp=timestamp,
                position=(0.0, 0.0, 0.0),
                rotation=(head_nod, 0.0, 0.0),
                blend_shape_weights=blend_shapes,
            )
            keyframes.append(keyframe)

        return keyframes

    def generate_gesture_motion(
        self, duration: float, gesture_type: str = "wave", fps: int = 30
    ) -> list[AnimationKeyframe]:
        """Generate gesture animations"""
        keyframes = []
        frame_count = int(duration * fps)

        if gesture_type == "wave":
            return self._generate_wave_gesture(duration, fps)
        elif gesture_type == "nod":
            return self._generate_nod_gesture(duration, fps)
        elif gesture_type == "point":
            return self._generate_point_gesture(duration, fps)
        else:
            # Default to subtle gesture
            return self.generate_idle_motion(duration, fps)

    def _generate_wave_gesture(
        self, duration: float, fps: int
    ) -> list[AnimationKeyframe]:
        """Generate waving gesture"""
        keyframes = []
        frame_count = int(duration * fps)
        wave_cycles = 2  # Number of waves

        for i in range(frame_count):
            timestamp = i / fps
            progress = timestamp / duration

            # Wave motion
            wave_angle = progress * wave_cycles * 2 * math.pi
            arm_rotation = math.sin(wave_angle) * 30.0  # 30 degree wave

            # Ease in/out
            ease_factor = 1.0 - abs(progress - 0.5) * 2
            arm_rotation *= ease_factor

            keyframe = AnimationKeyframe(
                timestamp=timestamp, rotation=(0.0, 0.0, math.radians(arm_rotation))
            )
            keyframes.append(keyframe)

        return keyframes

    def _generate_nod_gesture(
        self, duration: float, fps: int
    ) -> list[AnimationKeyframe]:
        """Generate nodding gesture"""
        keyframes = []
        frame_count = int(duration * fps)
        nod_cycles = 3  # Number of nods

        for i in range(frame_count):
            timestamp = i / fps
            progress = timestamp / duration

            # Nod motion
            nod_angle = progress * nod_cycles * 2 * math.pi
            head_rotation = math.sin(nod_angle) * 15.0  # 15 degree nod

            keyframe = AnimationKeyframe(
                timestamp=timestamp, rotation=(math.radians(head_rotation), 0.0, 0.0)
            )
            keyframes.append(keyframe)

        return keyframes

    def _generate_point_gesture(
        self, duration: float, fps: int
    ) -> list[AnimationKeyframe]:
        """Generate pointing gesture"""
        keyframes = []
        frame_count = int(duration * fps)

        for i in range(frame_count):
            timestamp = i / fps
            progress = timestamp / duration

            # Point gesture - raise arm and extend finger
            if progress < 0.3:  # Raise arm
                arm_lift = (progress / 0.3) * 45.0
            elif progress > 0.7:  # Lower arm
                arm_lift = ((1.0 - progress) / 0.3) * 45.0
            else:  # Hold position
                arm_lift = 45.0

            keyframe = AnimationKeyframe(
                timestamp=timestamp, rotation=(0.0, math.radians(arm_lift), 0.0)
            )
            keyframes.append(keyframe)

        return keyframes


class AnimationEngine:
    """Core animation engine for avatars"""

    def __init__(self, temp_dir: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.blend_shape_controller = BlendShapeController()
        self.motion_generator = MotionGenerator()

        # Create temp directory if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)

    def create_animation_sequence(self, request: AnimationRequest) -> AnimationSequence:
        """Create animation sequence from request"""
        try:
            # Generate keyframes based on animation type
            if request.animation_type == AnimationType.IDLE:
                keyframes = self.motion_generator.generate_idle_motion(
                    request.duration, request.fps
                )
            elif request.animation_type == AnimationType.TALKING:
                intensity = (
                    request.custom_parameters.get("speech_intensity", 1.0)
                    if request.custom_parameters
                    else 1.0
                )
                keyframes = self.motion_generator.generate_talking_motion(
                    request.duration, request.fps, intensity
                )
            elif request.animation_type == AnimationType.GESTURING:
                gesture_type = (
                    request.custom_parameters.get("gesture_type", "wave")
                    if request.custom_parameters
                    else "wave"
                )
                keyframes = self.motion_generator.generate_gesture_motion(
                    request.duration, gesture_type, request.fps
                )
            else:
                # Default to idle
                keyframes = self.motion_generator.generate_idle_motion(
                    request.duration, request.fps
                )

            # Apply emotion blend shapes to all keyframes
            emotion_weights = self.blend_shape_controller.get_emotion_weights(
                request.emotion
            )
            for keyframe in keyframes:
                if keyframe.blend_shape_weights is None:
                    keyframe.blend_shape_weights = {}

                # Merge emotion weights with existing blend shapes
                for shape, weight in emotion_weights.items():
                    if shape not in keyframe.blend_shape_weights:
                        keyframe.blend_shape_weights[shape] = weight
                    else:
                        # Blend with existing weight
                        keyframe.blend_shape_weights[shape] = (
                            keyframe.blend_shape_weights[shape] + weight
                        ) / 2.0

            sequence = AnimationSequence(
                name=f"{request.animation_type.value}_{request.emotion.value}",
                animation_type=request.animation_type,
                keyframes=keyframes,
                duration=request.duration,
                fps=request.fps,
                loop=request.loop,
                emotion=request.emotion,
            )

            return sequence

        except Exception as e:
            self.logger.error(f"Animation sequence creation failed: {e}")
            # Return empty sequence
            return AnimationSequence(
                name="error",
                animation_type=AnimationType.IDLE,
                keyframes=[],
                duration=0.0,
            )

    def export_animation(
        self, sequence: AnimationSequence, output_path: str, format: str = "json"
    ) -> bool:
        """Export animation sequence to file"""
        try:
            if format.lower() == "json":
                return self._export_to_json(sequence, output_path)
            elif format.lower() == "bvh":
                return self._export_to_bvh(sequence, output_path)
            else:
                self.logger.error(f"Unsupported export format: {format}")
                return False

        except Exception as e:
            self.logger.error(f"Animation export failed: {e}")
            return False

    def _export_to_json(self, sequence: AnimationSequence, output_path: str) -> bool:
        """Export animation to JSON format"""
        try:
            data = {
                "name": sequence.name,
                "animation_type": sequence.animation_type.value,
                "duration": sequence.duration,
                "fps": sequence.fps,
                "loop": sequence.loop,
                "emotion": sequence.emotion.value,
                "keyframes": [],
            }

            for keyframe in sequence.keyframes:
                keyframe_data = {
                    "timestamp": keyframe.timestamp,
                    "position": keyframe.position,
                    "rotation": keyframe.rotation,
                    "scale": keyframe.scale,
                    "blend_shape_weights": keyframe.blend_shape_weights or {},
                    "metadata": keyframe.metadata or {},
                }
                data["keyframes"].append(keyframe_data)

            with open(output_path, "w") as f:
                json.dump(data, f, indent=2)

            return True

        except Exception as e:
            self.logger.error(f"JSON export failed: {e}")
            return False

    def _export_to_bvh(self, sequence: AnimationSequence, output_path: str) -> bool:
        """Export animation to BVH format (simplified)"""
        try:
            # This is a simplified BVH export - in practice, you'd need
            # a proper BVH library or more complex implementation
            with open(output_path, "w") as f:
                f.write("HIERARCHY\n")
                f.write("ROOT Root\n")
                f.write("{\n")
                f.write("  OFFSET 0.0 0.0 0.0\n")
                f.write(
                    "  CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation\n"
                )
                f.write("}\n")
                f.write("MOTION\n")
                f.write(f"Frames: {len(sequence.keyframes)}\n")
                f.write(f"Frame Time: {1.0 / sequence.fps}\n")

                for keyframe in sequence.keyframes:
                    pos = keyframe.position
                    rot = keyframe.rotation
                    f.write(
                        f"{pos[0]} {pos[1]} {pos[2]} {math.degrees(rot[2])} {
                            math.degrees(rot[0])
                        } {math.degrees(rot[1])}\n"
                    )

            return True

        except Exception as e:
            self.logger.error(f"BVH export failed: {e}")
            return False

    async def process_animation(self, request: AnimationRequest) -> AnimationResult:
        """Process complete animation request"""
        start_time = datetime.now()

        try:
            # Create animation sequence
            sequence = self.create_animation_sequence(request)

            if not sequence.keyframes:
                return AnimationResult(
                    success=False, error="Failed to generate animation keyframes"
                )

            # Determine output path
            output_path = request.output_path
            if not output_path:
                base_name = f"avatar_animation_{request.animation_type.value}_{
                    request.emotion.value
                }"
                output_path = os.path.join(self.temp_dir, f"{base_name}.json")

            # Export animation
            export_format = "json"  # Default format
            if output_path.endswith(".bvh"):
                export_format = "bvh"

            success = self.export_animation(sequence, output_path, export_format)

            if not success:
                return AnimationResult(
                    success=False, error="Failed to export animation"
                )

            # Calculate quality score (simplified)
            quality_score = self._calculate_quality_score(sequence, request.quality)

            processing_time = (datetime.now() - start_time).total_seconds()

            return AnimationResult(
                success=True,
                output_path=output_path,
                duration=sequence.duration,
                frame_count=len(sequence.keyframes),
                processing_time=processing_time,
                animation_type=request.animation_type,
                quality_score=quality_score,
                metadata={
                    "emotion": request.emotion.value,
                    "fps": request.fps,
                    "loop": request.loop,
                    "export_format": export_format,
                },
            )

        except Exception as e:
            self.logger.error(f"Animation processing failed: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            return AnimationResult(
                success=False, error=str(e), processing_time=processing_time
            )

    def _calculate_quality_score(
        self, sequence: AnimationSequence, quality: QualityLevel
    ) -> float:
        """Calculate animation quality score"""
        try:
            # Base score from quality level
            quality_scores = {
                QualityLevel.LOW: 60.0,
                QualityLevel.MEDIUM: 75.0,
                QualityLevel.HIGH: 90.0,
                QualityLevel.ULTRA: 95.0,
            }

            base_score = quality_scores.get(quality, 75.0)

            # Adjust based on animation complexity
            keyframe_bonus = min(10.0, len(sequence.keyframes) / 100.0 * 10.0)

            # Adjust based on blend shape usage
            blend_shape_bonus = 0.0
            for keyframe in sequence.keyframes:
                if keyframe.blend_shape_weights:
                    blend_shape_bonus += len(keyframe.blend_shape_weights) * 0.1

            blend_shape_bonus = min(5.0, blend_shape_bonus)

            total_score = base_score + keyframe_bonus + blend_shape_bonus
            return min(100.0, total_score)

        except Exception as e:
            self.logger.error(f"Quality score calculation failed: {e}")
            return 50.0


class AvatarAnimator:
    """Main avatar animation class - high-level interface"""

    def __init__(self, temp_dir: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.engine = AnimationEngine(temp_dir)

        # Create temp directory if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)

    async def animate_avatar(
        self,
        avatar_path: str,
        animation_type: AnimationType,
        duration: float,
        emotion: EmotionType = EmotionType.NEUTRAL,
        output_path: Optional[str] = None,
        **kwargs,
    ) -> AnimationResult:
        """High-level avatar animation function"""
        request = AnimationRequest(
            avatar_path=avatar_path,
            animation_type=animation_type,
            duration=duration,
            emotion=emotion,
            output_path=output_path,
            **kwargs,
        )

        return await self.engine.process_animation(request)

    async def create_talking_avatar(
        self,
        avatar_path: str,
        duration: float,
        speech_intensity: float = 1.0,
        emotion: EmotionType = EmotionType.NEUTRAL,
        output_path: Optional[str] = None,
    ) -> AnimationResult:
        """Create talking avatar animation"""
        return await self.animate_avatar(
            avatar_path=avatar_path,
            animation_type=AnimationType.TALKING,
            duration=duration,
            emotion=emotion,
            output_path=output_path,
            custom_parameters={"speech_intensity": speech_intensity},
        )

    async def create_gesture_avatar(
        self,
        avatar_path: str,
        duration: float,
        gesture_type: str = "wave",
        emotion: EmotionType = EmotionType.NEUTRAL,
        output_path: Optional[str] = None,
    ) -> AnimationResult:
        """Create gesturing avatar animation"""
        return await self.animate_avatar(
            avatar_path=avatar_path,
            animation_type=AnimationType.GESTURING,
            duration=duration,
            emotion=emotion,
            output_path=output_path,
            custom_parameters={"gesture_type": gesture_type},
        )

    def get_supported_animations(self) -> list[AnimationType]:
        """Get list of supported animation types"""
        return list(AnimationType)

    def get_supported_emotions(self) -> list[EmotionType]:
        """Get list of supported emotions"""
        return list(EmotionType)

    def get_system_info(self) -> dict[str, Any]:
        """Get system information and capabilities"""
        return {
            "numpy_available": np is not None,
            "pil_available": Image is not None,
            "opencv_available": cv2 is not None,
            "supported_animations": [
                anim.value for anim in self.get_supported_animations()
            ],
            "supported_emotions": [
                emotion.value for emotion in self.get_supported_emotions()
            ],
            "temp_directory": self.temp_dir,
        }


# Convenience functions
async def animate_avatar(
    avatar_path: str,
    animation_type: AnimationType,
    duration: float,
    emotion: EmotionType = EmotionType.NEUTRAL,
    output_path: Optional[str] = None,
) -> AnimationResult:
    """Convenience function for avatar animation"""
    animator = AvatarAnimator()
    return await animator.animate_avatar(
        avatar_path, animation_type, duration, emotion, output_path
    )


async def create_talking_avatar(
    avatar_path: str,
    duration: float,
    speech_intensity: float = 1.0,
    emotion: EmotionType = EmotionType.NEUTRAL,
    output_path: Optional[str] = None,
) -> AnimationResult:
    """Convenience function for talking avatar"""
    animator = AvatarAnimator()
    return await animator.create_talking_avatar(
        avatar_path, duration, speech_intensity, emotion, output_path
    )


async def create_gesture_avatar(
    avatar_path: str,
    duration: float,
    gesture_type: str = "wave",
    emotion: EmotionType = EmotionType.NEUTRAL,
    output_path: Optional[str] = None,
) -> AnimationResult:
    """Convenience function for gesture avatar"""
    animator = AvatarAnimator()
    return await animator.create_gesture_avatar(
        avatar_path, duration, gesture_type, emotion, output_path
    )


def get_animation_info() -> dict[str, Any]:
    """Get information about animation capabilities"""
    animator = AvatarAnimator()
    return animator.get_system_info()
