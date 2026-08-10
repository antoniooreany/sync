import shutil
from pathlib import Path
from feature_sync.constants import FEATURES

def get_porter_features() -> dict:
    """Return catalog of porter features."""
    return FEATURES

def copy_feature_configs(feature_key: str, target_dir: Path) -> list[Path]:
    """Copy configs or templates associated with a feature to target directory."""
    copied = []
    
    # We will simulate copying configurations or setting up default files
    if feature_key == "gitlint_sync":
        # Create default .gitlint configuration
        gitlint_conf = target_dir / ".gitlint"
        if not gitlint_conf.exists():
            from gitlint_sync.core import generate_gitlint_config
            gitlint_conf.write_text(generate_gitlint_config(), encoding="utf-8")
            copied.append(gitlint_conf)
            
    elif feature_key == "gitflow_sync":
        # Ensure we have git configurations or files if needed
        pass
        
    return copied
