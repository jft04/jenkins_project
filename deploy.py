import importlib.util
import os
import shutil
import sys
from datetime import datetime

FILES_TO_DEPLOY = ["app.py", "requirements.txt"]
DEFAULT_DEPLOY_DIR = os.path.join("C:\\", "deployments", "jenkins_project")
EXPECTED_OUTPUT = "Hello, World from Jad Tannir!"


def copy_files(deploy_dir):
    os.makedirs(deploy_dir, exist_ok=True)
    for name in FILES_TO_DEPLOY:
        shutil.copy2(name, os.path.join(deploy_dir, name))
        print(f"Copied {name} -> {deploy_dir}")


def write_version_file(deploy_dir):
    build = os.environ.get("BUILD_NUMBER", "local")
    commit = os.environ.get("GIT_COMMIT", "unknown")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(deploy_dir, "VERSION.txt"), "w") as f:
        f.write(f"Build: {build}\nCommit: {commit}\nDeployed at: {time}\n")
    print(f"Wrote VERSION.txt (build {build})")


def smoke_test(deploy_dir):
    path = os.path.join(deploy_dir, "app.py")
    spec = importlib.util.spec_from_file_location("deployed_app", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.greet("World")
    print(f"Smoke test output: {result}")
    return result == EXPECTED_OUTPUT


def main():
    deploy_dir = os.environ.get("DEPLOY_DIR", DEFAULT_DEPLOY_DIR)
    print(f"Deploying application to {deploy_dir}")
    copy_files(deploy_dir)
    write_version_file(deploy_dir)
    if not smoke_test(deploy_dir):
        print("Smoke test FAILED - deployment is broken")
        sys.exit(1)
    print("Smoke test passed - deployment successful")


if __name__ == "__main__":
    main()
