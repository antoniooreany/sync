import sys
from pathlib import Path
from feature_sync.constants import EXIT_CODE_SUCCESS, EXIT_CODE_EXPECTED_ERROR
from feature_sync.core import get_porter_features, copy_feature_configs

def main():
    # Reconfigure console output encoding on Windows to support emojis
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    features = get_porter_features()

    print("🚀 Welcome to Sync Feature Porter CLI!")
    print("This interactive guide helps you port automation tools to your current project.\n")
    print("Available features:")
    
    keys = list(features.keys())
    for idx, key in enumerate(keys, 1):
        feat = features[key]
        print(f"  [{idx}] {feat['name']}")
        print(f"      {feat['desc']}")

    try:
        ans = input("\n👉 Select a feature number to learn more & initialize: ").strip()
        if not ans.isdigit():
            print("❌ Invalid selection. Please enter a number.", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

        choice_idx = int(ans) - 1
        if choice_idx < 0 or choice_idx >= len(keys):
            print("❌ Selection out of range.", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

        selected_key = keys[choice_idx]
        feat = features[selected_key]

        print(f"\n--- {feat['name']} ---")
        print(feat['desc'])
        
        setup_ans = input(f"\n❓ Do you want to initialize/port configurations for '{selected_key}' here? [y/N]: ").strip().lower()
        if setup_ans in ["y", "yes"]:
            target_dir = Path.cwd()
            copied = copy_feature_configs(selected_key, target_dir)
            if copied:
                print("\n🎉 Config files written:")
                for c in copied:
                    print(f"  • {c.relative_to(target_dir)}")
            else:
                print("\n🎉 Ready! No static configuration files required to start.")
            
            print("\n💡 What to do next:")
            for step in feat["next_steps"]:
                print(f"  • {step}")
        else:
            print("\nSkipped initialization.")

    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(EXIT_CODE_SUCCESS)

if __name__ == "__main__":
    main()
