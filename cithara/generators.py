from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import requests

@dataclass
class SongGenerationRequest:
    """Standardizes the data we send to any generator."""
    title: str
    tags: str
    prompt: str

@dataclass
class SongGenerationResult:
    """Standardizes the output we get back from any generator."""
    task_id: str
    status: str
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    error: Optional[str] = None

class SongGeneratorStrategy(ABC):
    """The abstract base class (interface) for all generators."""
    
    @abstractmethod
    def generate(self, request: SongGenerationRequest) -> SongGenerationResult:
        """Starts the generation process."""
        pass
    
    @abstractmethod
    def check_status(self, task_id: str) -> SongGenerationResult:
        """Checks the status of an ongoing generation."""
        pass


class MockSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Does not call any external API. 
    Produces predictable output for testing.
    """
    def generate(self, request: SongGenerationRequest) -> SongGenerationResult:
        return SongGenerationResult(
            task_id="mock-task-12345",
            status="PENDING" 
        )

    def check_status(self, task_id: str) -> SongGenerationResult:
        return SongGenerationResult(
            task_id=task_id,
            status="SUCCESS",
            audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", 
            video_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        )


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Integrates with SunoApi.org to generate real music.
    """
    BASE_URL = "https://api.sunoapi.org/api/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate(self, request: SongGenerationRequest) -> SongGenerationResult:
        """1.3.1 Create generation task via POST"""
        url = f"{self.BASE_URL}/generate"
        payload = {
            "title": request.title,
            "tags": request.tags,
            "prompt": request.prompt,
            "make_instrumental": False
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            task_id = data.get("data", {}).get("taskId") or data.get("taskId")
            
            if not task_id:
                return SongGenerationResult(task_id="", status="FAILED", error="API did not return a taskId")
                
            return SongGenerationResult(task_id=task_id, status="PENDING")
            
        except Exception as e:
            return SongGenerationResult(task_id="", status="FAILED", error=str(e))

    def check_status(self, task_id: str) -> SongGenerationResult:
        """1.3.3 Check generation status/results via GET polling"""
        url = f"{self.BASE_URL}/generate/record-info"
        params = {"taskId": task_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            record = data.get("data", {})
            if isinstance(record, list) and len(record) > 0:
                record = record[0] 

            status = record.get("status", "PENDING")
            audio_url = record.get("audioUrl") or record.get("audio_url")
            video_url = record.get("videoUrl") or record.get("video_url")
            
            return SongGenerationResult(
                task_id=task_id,
                status=status,
                audio_url=audio_url,
                video_url=video_url
            )

        except Exception as e:
            return SongGenerationResult(task_id=task_id, status="FAILED", error=str(e))
