"""
Main entry point for AI Navigator application
Predictive incident detection platform with GigaChat API integration
"""

import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv
import os

from app.services.anonymizer import PIIAnonymizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def initialize_app() -> Optional[PIIAnonymizer]:
    """
    Initialize the AI Navigator application
    
    Returns:
        PIIAnonymizer: Anonymizer service for data protection
    """
    try:
        logger.info("🚀 Initializing AI Navigator...")
        
        # Load environment variables
        load_dotenv()
        gigachat_api_key = os.getenv("GIGACHAT_API_KEY")
        
        if not gigachat_api_key:
            logger.error("❌ GIGACHAT_API_KEY not found in environment variables")
            return None
        
        logger.info("✅ Environment variables loaded")
        
        # Initialize PII Anonymizer
        anonymizer = PIIAnonymizer()
        logger.info("✅ PII Anonymizer initialized")
        
        return anonymizer
        
    except Exception as e:
        logger.error(f"❌ Initialization error: {str(e)}", exc_info=True)
        return None


async def main():
    """
    Main application entry point
    """
    logger.info("=" * 60)
    logger.info("AI Navigator - Predictive Incident Detection")
    logger.info("=" * 60)
    
    # Initialize application
    anonymizer = await initialize_app()
    
    if anonymizer is None:
        logger.error("❌ Failed to initialize application")
        return
    
    try:
        logger.info("✅ Application initialized successfully")
        logger.info("🔄 Ready to process incidents...")
        
        # Application main loop would go here
        # This is a placeholder for the main incident processing logic
        
        logger.info("✅ Application running...")
        
    except KeyboardInterrupt:
        logger.info("⏸️  Application interrupted by user")
    except Exception as e:
        logger.error(f"❌ Application error: {str(e)}", exc_info=True)
    finally:
        logger.info("🛑 Shutting down AI Navigator...")


if __name__ == "__main__":
    asyncio.run(main())
