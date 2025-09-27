"""Audio Post-Production Module - Advanced audio processing and enhancement system"""

import os
import logging
from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import tempfile

# Optional imports with fallbacks
try:
    import numpy as np
except ImportError:
    np = None

try:
    from scipy import signal
    from scipy.io import wavfile
except ImportError:
    signal = None
    wavfile = None

try:
    import librosa
except ImportError:
    librosa = None

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None


class AudioFormat(Enum):
    """Supported audio formats"""

    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    AAC = "aac"
    OGG = "ogg"
    M4A = "m4a"


class ProcessingType(Enum):
    """Types of audio processing"""

    NOISE_REDUCTION = "noise_reduction"
    NORMALIZATION = "normalization"
    COMPRESSION = "compression"
    EQ = "equalization"
    REVERB = "reverb"
    DELAY = "delay"
    PITCH_CORRECTION = "pitch_correction"
    VOCAL_ENHANCEMENT = "vocal_enhancement"
    MASTERING = "mastering"
    CUSTOM = "custom"


class QualityLevel(Enum):
    """Audio quality levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    STUDIO = "studio"


class AudioChannel(Enum):
    """Audio channel configurations"""

    MONO = "mono"
    STEREO = "stereo"
    SURROUND_5_1 = "surround_5_1"
    SURROUND_7_1 = "surround_7_1"


@dataclass
class AudioMetadata:
    """Audio file metadata"""

    duration: float
    sample_rate: int
    channels: int
    bit_depth: Optional[int] = None
    format: Optional[AudioFormat] = None
    file_size: Optional[int] = None
    peak_amplitude: Optional[float] = None
    rms_level: Optional[float] = None
    dynamic_range: Optional[float] = None
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ProcessingParameters:
    """Parameters for audio processing"""

    processing_type: ProcessingType
    intensity: float = 1.0
    frequency_range: Optional[tuple[float, float]] = None
    threshold: Optional[float] = None
    ratio: Optional[float] = None
    attack_time: Optional[float] = None
    release_time: Optional[float] = None
    custom_params: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.custom_params is None:
            self.custom_params = {}


@dataclass
class AudioProcessingRequest:
    """Request for audio processing"""

    input_path: str
    output_path: Optional[str] = None
    processing_chain: Optional[list[ProcessingParameters]] = None
    target_format: AudioFormat = AudioFormat.WAV
    target_quality: QualityLevel = QualityLevel.HIGH
    target_sample_rate: Optional[int] = None
    target_channels: Optional[AudioChannel] = None
    normalize_output: bool = True
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.processing_chain is None:
            self.processing_chain = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AudioProcessingResult:
    """Result of audio processing"""

    success: bool
    output_path: Optional[str] = None
    original_metadata: Optional[AudioMetadata] = None
    processed_metadata: Optional[AudioMetadata] = None
    processing_time: Optional[float] = None
    quality_score: Optional[float] = None
    applied_effects: Optional[list[str]] = None
    error: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.applied_effects is None:
            self.applied_effects = []
        if self.metadata is None:
            self.metadata = {}


class AudioAnalyzer:
    """Analyzes audio files and extracts metadata"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_audio(self, file_path: str) -> Optional[AudioMetadata]:
        """Analyze audio file and extract metadata"""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"Audio file not found: {file_path}")
                return None

            # Try different methods based on available libraries
            if librosa is not None:
                return self._analyze_with_librosa(file_path)
            elif AudioSegment is not None:
                return self._analyze_with_pydub(file_path)
            else:
                return self._analyze_basic(file_path)

        except Exception as e:
            self.logger.error(f"Audio analysis failed: {e}")
            return None

    def _analyze_with_librosa(self, file_path: str) -> AudioMetadata:
        """Analyze using librosa library"""
        if librosa is None:
            raise ImportError("librosa not available")
        y, sr = librosa.load(file_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)

        # Calculate audio statistics
        peak_amplitude = float(np.max(np.abs(y))) if np is not None else 0.0
        rms_level = float(np.sqrt(np.mean(y**2))) if np is not None else 0.0

        return AudioMetadata(
            duration=duration,
            sample_rate=sr,
            channels=1 if len(y.shape) == 1 else y.shape[0],
            peak_amplitude=peak_amplitude,
            rms_level=rms_level,
            file_size=os.path.getsize(file_path),
        )

    def _analyze_with_pydub(self, file_path: str) -> AudioMetadata:
        """Analyze using pydub library"""
        if AudioSegment is None:
            raise ImportError("AudioSegment not available")
        audio = AudioSegment.from_file(file_path)

        return AudioMetadata(
            duration=len(audio) / 1000.0,  # Convert ms to seconds
            sample_rate=audio.frame_rate,
            channels=audio.channels,
            file_size=os.path.getsize(file_path),
        )

    def _analyze_basic(self, file_path: str) -> AudioMetadata:
        """Basic analysis without external libraries"""
        file_size = os.path.getsize(file_path)

        # Estimate basic properties (simplified)
        return AudioMetadata(
            duration=0.0,  # Cannot determine without audio library
            sample_rate=44100,  # Default assumption
            channels=2,  # Default assumption
            file_size=file_size,
        )

    def detect_silence(
        self, file_path: str, threshold: float = -40.0
    ) -> list[tuple[float, float]]:
        """Detect silent segments in audio"""
        try:
            if AudioSegment is None:
                return []

            audio = AudioSegment.from_file(file_path)
            silence_ranges = []

            # Simple silence detection
            chunk_size = 100  # ms
            for i in range(0, len(audio), chunk_size):
                chunk = audio[i : i + chunk_size]
                if chunk.dBFS < threshold:
                    start_time = i / 1000.0
                    end_time = min(i + chunk_size, len(audio)) / 1000.0
                    silence_ranges.append((start_time, end_time))

            return silence_ranges

        except Exception as e:
            self.logger.error(f"Silence detection failed: {e}")
            return []


class AudioProcessor:
    """Core audio processing engine"""

    def __init__(self, temp_dir: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.analyzer = AudioAnalyzer()

        # Create temp directory if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)

    def apply_noise_reduction(
        self, audio_data: Any, sample_rate: int, intensity: float = 1.0
    ) -> Any:
        """Apply noise reduction to audio data"""
        try:
            if np is None or signal is None:
                self.logger.warning("NumPy or SciPy not available for noise reduction")
                return audio_data

            # Simple spectral subtraction noise reduction
            # This is a simplified implementation
            if len(audio_data.shape) > 1:
                # Process each channel separately
                processed = np.zeros_like(audio_data)
                for i in range(audio_data.shape[0]):
                    processed[i] = self._spectral_subtraction(audio_data[i], intensity)
                return processed
            else:
                return self._spectral_subtraction(audio_data, intensity)

        except Exception as e:
            self.logger.error(f"Noise reduction failed: {e}")
            return audio_data

    def _spectral_subtraction(self, audio: Any, intensity: float) -> Any:
        """Apply spectral subtraction noise reduction"""
        if np is None:
            return audio

        # Simple high-pass filter as noise reduction
        nyquist = 0.5
        cutoff = 80.0 / (22050 * nyquist)  # 80 Hz cutoff

        if signal is not None:
            b, a = signal.butter(4, cutoff, btype="high")
            filtered = signal.filtfilt(b, a, audio)
            return audio * (1 - intensity) + filtered * intensity

        return audio

    def apply_normalization(self, audio_data: Any, target_level: float = -3.0) -> Any:
        """Normalize audio to target level"""
        try:
            if np is None:
                return audio_data

            # Calculate current peak level
            peak = np.max(np.abs(audio_data))

            if peak == 0:
                return audio_data

            # Calculate normalization factor
            target_linear = 10 ** (target_level / 20.0)
            normalization_factor = target_linear / peak

            return audio_data * normalization_factor

        except Exception as e:
            self.logger.error(f"Normalization failed: {e}")
            return audio_data

    def apply_compression(
        self,
        audio_data: Any,
        threshold: float = -12.0,
        ratio: float = 4.0,
        attack: float = 0.003,
        release: float = 0.1,
    ) -> Any:
        """Apply dynamic range compression"""
        try:
            if np is None:
                return audio_data

            # Simple compression implementation
            threshold_linear = 10 ** (threshold / 20.0)
            compressed = np.copy(audio_data)

            # Find samples above threshold
            above_threshold = np.abs(compressed) > threshold_linear

            # Apply compression to samples above threshold
            compressed[above_threshold] = np.sign(compressed[above_threshold]) * (
                threshold_linear
                + (np.abs(compressed[above_threshold]) - threshold_linear) / ratio
            )

            return compressed

        except Exception as e:
            self.logger.error(f"Compression failed: {e}")
            return audio_data

    def apply_eq(
        self,
        audio_data: Any,
        sample_rate: int,
        frequency: float,
        gain: float,
        q_factor: float = 1.0,
    ) -> Any:
        """Apply parametric EQ"""
        try:
            if np is None or signal is None:
                return audio_data

            # Design peaking EQ filter
            nyquist = sample_rate / 2.0
            freq_norm = frequency / nyquist

            if freq_norm >= 1.0 or freq_norm <= 0.0:
                return audio_data

            # Simple peaking filter
            b, a = signal.iirpeak(freq_norm, q_factor)

            # Apply gain
            if gain != 0:
                gain_linear = 10 ** (gain / 20.0)
                filtered = signal.filtfilt(b, a, audio_data)
                return audio_data + (filtered - audio_data) * (gain_linear - 1)

            return audio_data

        except Exception as e:
            self.logger.error(f"EQ failed: {e}")
            return audio_data

    def process_audio_file(
        self, request: AudioProcessingRequest
    ) -> AudioProcessingResult:
        """Process audio file with specified parameters"""
        start_time = datetime.now()

        try:
            # Analyze input file
            original_metadata = self.analyzer.analyze_audio(request.input_path)
            if not original_metadata:
                return AudioProcessingResult(
                    success=False, error="Failed to analyze input audio file"
                )

            # Load audio data
            if librosa is not None:
                audio_data, sample_rate = librosa.load(request.input_path, sr=None)
            elif AudioSegment is not None:
                audio_segment = AudioSegment.from_file(request.input_path)
                audio_data = (
                    np.array(audio_segment.get_array_of_samples())
                    if np is not None
                    else None
                )
                sample_rate = audio_segment.frame_rate
            else:
                return AudioProcessingResult(
                    success=False, error="No audio processing library available"
                )

            if audio_data is None:
                return AudioProcessingResult(
                    success=False, error="Failed to load audio data"
                )

            # Apply processing chain
            processed_audio = audio_data
            applied_effects = []

            for params in request.processing_chain or []:
                if params.processing_type == ProcessingType.NOISE_REDUCTION:
                    processed_audio = self.apply_noise_reduction(
                        processed_audio, sample_rate, params.intensity
                    )
                    applied_effects.append("noise_reduction")

                elif params.processing_type == ProcessingType.NORMALIZATION:
                    target_level = (
                        params.custom_params.get("target_level", -3.0)
                        if params.custom_params
                        else -3.0
                    )
                    processed_audio = self.apply_normalization(
                        processed_audio, target_level
                    )
                    applied_effects.append("normalization")

                elif params.processing_type == ProcessingType.COMPRESSION:
                    threshold = params.threshold or -12.0
                    ratio = params.ratio or 4.0
                    processed_audio = self.apply_compression(
                        processed_audio, threshold, ratio
                    )
                    applied_effects.append("compression")

                elif params.processing_type == ProcessingType.EQ:
                    if params.frequency_range and params.custom_params:
                        freq = params.frequency_range[0]
                        gain = params.custom_params.get("gain", 0.0)
                        q = params.custom_params.get("q_factor", 1.0)
                        processed_audio = self.apply_eq(
                            processed_audio, sample_rate, freq, gain, q
                        )
                        applied_effects.append("eq")

            # Apply final normalization if requested
            if request.normalize_output:
                processed_audio = self.apply_normalization(processed_audio)
                if "normalization" not in applied_effects:
                    applied_effects.append("final_normalization")

            # Determine output path
            output_path = request.output_path
            if not output_path:
                base_name = os.path.splitext(os.path.basename(request.input_path))[0]
                output_path = os.path.join(
                    self.temp_dir,
                    f"{base_name}_processed.{request.target_format.value}",
                )

            # Save processed audio
            success = self._save_audio(
                processed_audio, sample_rate, output_path, request.target_format
            )

            if not success:
                return AudioProcessingResult(
                    success=False, error="Failed to save processed audio"
                )

            # Analyze processed audio
            processed_metadata = self.analyzer.analyze_audio(output_path)

            # Calculate quality score
            quality_score = self._calculate_quality_score(
                original_metadata, processed_metadata
            )

            processing_time = (datetime.now() - start_time).total_seconds()

            return AudioProcessingResult(
                success=True,
                output_path=output_path,
                original_metadata=original_metadata,
                processed_metadata=processed_metadata,
                processing_time=processing_time,
                quality_score=quality_score,
                applied_effects=applied_effects,
            )

        except Exception as e:
            self.logger.error(f"Audio processing failed: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            return AudioProcessingResult(
                success=False, error=str(e), processing_time=processing_time
            )

    def _save_audio(
        self, audio_data: Any, sample_rate: int, output_path: str, format: AudioFormat
    ) -> bool:
        """Save processed audio to file"""
        try:
            if AudioSegment is not None and np is not None:
                # Convert numpy array to AudioSegment
                audio_int16 = (audio_data * 32767).astype(np.int16)
                audio_segment = AudioSegment(
                    audio_int16.tobytes(),
                    frame_rate=sample_rate,
                    sample_width=2,
                    channels=1 if len(audio_data.shape) == 1 else audio_data.shape[0],
                )

                # Export in requested format
                audio_segment.export(output_path, format=format.value)
                return True

            elif wavfile is not None and format == AudioFormat.WAV:
                # Use scipy for WAV files
                wavfile.write(output_path, sample_rate, audio_data)
                return True

            else:
                self.logger.error("No suitable library for audio export")
                return False

        except Exception as e:
            self.logger.error(f"Audio save failed: {e}")
            return False

    def _calculate_quality_score(
        self, original: Optional[AudioMetadata], processed: Optional[AudioMetadata]
    ) -> float:
        """Calculate quality score for processed audio"""
        try:
            if not original or not processed:
                return 50.0

            score = 70.0  # Base score

            # Check if processing improved dynamic range
            if (
                original.dynamic_range
                and processed.dynamic_range
                and processed.dynamic_range > original.dynamic_range
            ):
                score += 10.0

            # Check if RMS level is appropriate
            if processed.rms_level and 0.1 <= processed.rms_level <= 0.7:
                score += 10.0

            # Check if peak amplitude is not clipping
            if processed.peak_amplitude and processed.peak_amplitude < 0.95:
                score += 10.0

            return min(100.0, score)

        except Exception as e:
            self.logger.error(f"Quality score calculation failed: {e}")
            return 50.0


class AudioPostProduction:
    """Main audio post-production class - high-level interface"""

    def __init__(self, temp_dir: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.processor = AudioProcessor(temp_dir)

        # Create temp directory if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)

    async def enhance_audio(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        enhancement_level: str = "medium",
    ) -> AudioProcessingResult:
        """Enhance audio with automatic processing chain"""
        # Define enhancement presets
        presets = {
            "light": [
                ProcessingParameters(ProcessingType.NORMALIZATION, intensity=0.8)
            ],
            "medium": [
                ProcessingParameters(ProcessingType.NOISE_REDUCTION, intensity=0.6),
                ProcessingParameters(
                    ProcessingType.COMPRESSION, threshold=-15.0, ratio=3.0
                ),
                ProcessingParameters(ProcessingType.NORMALIZATION, intensity=1.0),
            ],
            "heavy": [
                ProcessingParameters(ProcessingType.NOISE_REDUCTION, intensity=0.8),
                ProcessingParameters(
                    ProcessingType.COMPRESSION, threshold=-12.0, ratio=4.0
                ),
                ProcessingParameters(
                    ProcessingType.EQ, frequency_range=(100.0, 8000.0)
                ),
                ProcessingParameters(ProcessingType.NORMALIZATION, intensity=1.0),
            ],
        }

        processing_chain = presets.get(enhancement_level, presets["medium"])

        request = AudioProcessingRequest(
            input_path=input_path,
            output_path=output_path,
            processing_chain=processing_chain,
        )

        return self.processor.process_audio_file(request)

    async def master_audio(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        target_lufs: float = -14.0,
    ) -> AudioProcessingResult:
        """Master audio for broadcast/streaming standards"""
        mastering_chain = [
            ProcessingParameters(
                ProcessingType.EQ,
                frequency_range=(20.0, 20000.0),
                custom_params={"gain": 1.0, "q_factor": 0.7},
            ),
            ProcessingParameters(
                ProcessingType.COMPRESSION, threshold=-18.0, ratio=2.5
            ),
            ProcessingParameters(
                ProcessingType.NORMALIZATION,
                custom_params={"target_level": target_lufs},
            ),
        ]

        request = AudioProcessingRequest(
            input_path=input_path,
            output_path=output_path,
            processing_chain=mastering_chain,
            target_quality=QualityLevel.STUDIO,
        )

        return self.processor.process_audio_file(request)

    def get_system_info(self) -> dict[str, Any]:
        """Get system information and capabilities"""
        return {
            "numpy_available": np is not None,
            "scipy_available": signal is not None and wavfile is not None,
            "librosa_available": librosa is not None,
            "pydub_available": AudioSegment is not None,
            "supported_formats": [fmt.value for fmt in AudioFormat],
            "supported_processing": [proc.value for proc in ProcessingType],
            "temp_directory": self.temp_dir,
        }


# Convenience functions
async def enhance_audio(
    input_path: str,
    output_path: Optional[str] = None,
    enhancement_level: str = "medium",
) -> AudioProcessingResult:
    """Convenience function for audio enhancement"""
    processor = AudioPostProduction()
    return await processor.enhance_audio(input_path, output_path, enhancement_level)


async def master_audio(
    input_path: str, output_path: Optional[str] = None, target_lufs: float = -14.0
) -> AudioProcessingResult:
    """Convenience function for audio mastering"""
    processor = AudioPostProduction()
    return await processor.master_audio(input_path, output_path, target_lufs)


def analyze_audio_file(file_path: str) -> Optional[AudioMetadata]:
    """Convenience function for audio analysis"""
    analyzer = AudioAnalyzer()
    return analyzer.analyze_audio(file_path)


def get_audio_info() -> dict[str, Any]:
    """Get information about audio processing capabilities"""
    processor = AudioPostProduction()
    return processor.get_system_info()
