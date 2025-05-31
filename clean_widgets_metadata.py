import os
import nbformat

def clean_notebook_metadata(file_path):
    try:
        nb = nbformat.read(file_path, as_version=nbformat.NO_CONVERT)
        metadata_changed = False

        if "widgets" in nb.metadata:
            widgets = nb.metadata["widgets"]
            if isinstance(widgets, dict):
                if "application/vnd.jupyter.widget-state+json" in widgets:
                    widget_meta = widgets["application/vnd.jupyter.widget-state+json"]
                    if "state" not in widget_meta:
                        print(f"Fixing missing 'state' in: {file_path}")
                        widget_meta["state"] = {}
                        metadata_changed = True

        if metadata_changed:
            nbformat.write(nb, file_path)
            print(f"✅ Updated: {file_path}")
        else:
            print(f"👍 No changes needed: {file_path}")

    except Exception as e:
        print(f"❌ Failed to process {file_path}: {e}")

def walk_and_clean(directory="."):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipynb"):
                full_path = os.path.join(root, file)
                clean_notebook_metadata(full_path)

# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser(description="Clean broken widget metadata in Jupyter notebooks.")
#     parser.add_argument("--path", type=str, default=".", help="Directory to scan (default: current folder)")
#     args = parser.parse_args()

#     walk_and_clean(args.path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean broken widget metadata in Jupyter notebooks.")
    parser.add_argument("--path", type=str, required=True, help="Path to .ipynb file or directory")
    args = parser.parse_args()

    if args.path.endswith(".ipynb") and os.path.isfile(args.path):
        clean_notebook_metadata(args.path)  # Handle single notebook
    else:
        walk_and_clean(args.path)  # Handle directory

