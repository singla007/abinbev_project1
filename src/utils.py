import os
from pathlib import Path
from src.logger import get_logger

logger = get_logger(__name__)

def load_markdown_files(data_path):
    logger.info(f"Loading markdown files from: {data_path}")
    
    documents = []
    
    try:
        md_files = list(Path(data_path).rglob("*.md"))
        logger.info(f"Found {len(md_files)} markdown files.")
        
        for file_path in md_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    documents.append((str(file_path), content))
                    logger.debug(f"Loaded file: {file_path}")
            except Exception as e:
                logger.warning(f"Could not read file {file_path}: {e}")
                
    except Exception as e:
        logger.error(f"Error while accessing markdown files in {data_path}: {e}")
        raise

    logger.info(f"Total successfully loaded markdown files: {len(documents)}")
    return documents