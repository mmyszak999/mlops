#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
from pathlib import Path


# =========================================================
# Paths
# =========================================================

# cleanup.py is expected to be located in:
# ml/azure/cleanup.py
#
# Repository root:
REPO_ROOT = Path(__file__).resolve().parents[2]

TERRAFORM_DIR = REPO_ROOT / "terraform" / "azure"


# =========================================================
# Azure configuration
# =========================================================

AZURE_RESOURCE_GROUP = "mlops-thesis-azure"
AZURE_ML_WORKSPACE = "mlops-thesis-aml"

ENDPOINT_NAME = "titanic-random-forest"
MODEL_NAME = "titanic-random-forest"


# =========================================================
# Helpers
# =========================================================

def resolve_command(command: str) -> str:
    """
    Resolve a command in a cross-platform way.

    On Windows Azure CLI is commonly exposed as az.cmd.
    """

    if os.name == "nt":
        candidates = [
            f"{command}.cmd",
            f"{command}.exe",
            command,
        ]
    else:
        candidates = [command]

    for candidate in candidates:
        path = shutil.which(candidate)

        if path:
            return path

    raise FileNotFoundError(
        f"Command '{command}' was not found in PATH."
    )


def run_command(
    command: list[str],
    *,
    cwd: Path | None = None,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:

    if not command:
        raise ValueError(
            "Command cannot be empty."
        )

    resolved_command = [
        resolve_command(command[0]),
        *command[1:],
    ]

    return subprocess.run(
        resolved_command,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=capture_output,
    )


def command_exists(command: str) -> bool:
    try:
        resolve_command(command)
        return True

    except FileNotFoundError:
        return False


def azure_cli_available() -> bool:
    return command_exists("az")


def terraform_available() -> bool:
    return command_exists("terraform")


# =========================================================
# Azure ML cleanup
# =========================================================

def delete_endpoint() -> None:

    print()
    print("Checking Azure ML endpoint...")

    result = run_command(
        [
            "az",
            "ml",
            "online-endpoint",
            "show",
            "--name",
            ENDPOINT_NAME,
            "--resource-group",
            AZURE_RESOURCE_GROUP,
            "--workspace-name",
            AZURE_ML_WORKSPACE,
            "--query",
            "name",
            "-o",
            "tsv",
        ],
        capture_output=True,
    )

    if result.returncode != 0:

        print(
            f"Endpoint does not exist: {ENDPOINT_NAME}"
        )

        return

    print(
        f"Deleting Azure ML endpoint: "
        f"{ENDPOINT_NAME}"
    )

    result = run_command(
        [
            "az",
            "ml",
            "online-endpoint",
            "delete",
            "--name",
            ENDPOINT_NAME,
            "--resource-group",
            AZURE_RESOURCE_GROUP,
            "--workspace-name",
            AZURE_ML_WORKSPACE,
            "--yes",
        ]
    )

    if result.returncode != 0:

        raise RuntimeError(
            "Failed to delete Azure ML endpoint."
        )

    print(
        f"Endpoint deleted: {ENDPOINT_NAME}"
    )


# =========================================================
# Azure ML model cleanup
# =========================================================

def list_model_versions() -> list[str]:

    print()
    print(
        f"Checking registered model: "
        f"{MODEL_NAME}"
    )

    result = run_command(
        [
            "az",
            "ml",
            "model",
            "list",
            "--name",
            MODEL_NAME,
            "--resource-group",
            AZURE_RESOURCE_GROUP,
            "--workspace-name",
            AZURE_ML_WORKSPACE,
            "--query",
            "[].version",
            "-o",
            "tsv",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        return []

    versions = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    return versions


def delete_model_versions() -> None:

    versions = list_model_versions()

    if not versions:

        print(
            f"No registered versions found for: "
            f"{MODEL_NAME}"
        )

        return

    print()
    print(
        f"Found {len(versions)} registered model "
        f"version(s):"
    )

    for version in versions:
        print(f"  - version {version}")

    print()
    print("Deleting registered model versions...")

    for version in versions:

        print(
            f"Deleting model "
            f"{MODEL_NAME}:{version}"
        )

        result = run_command(
            [
                "az",
                "ml",
                "model",
                "delete",
                "--name",
                MODEL_NAME,
                "--version",
                version,
                "--resource-group",
                AZURE_RESOURCE_GROUP,
                "--workspace-name",
                AZURE_ML_WORKSPACE,
                "--yes",
            ]
        )

        if result.returncode != 0:

            raise RuntimeError(
                f"Failed to delete model version "
                f"{version}."
            )

    print(
        "Model versions deleted."
    )


# =========================================================
# Terraform cleanup
# =========================================================

def terraform_destroy() -> None:

    print()
    print("Running Terraform destroy...")
    print()

    if not TERRAFORM_DIR.exists():

        raise RuntimeError(
            f"Terraform directory does not exist: "
            f"{TERRAFORM_DIR}"
        )

    result = run_command(
        [
            "terraform",
            "destroy",
            "-auto-approve",
        ],
        cwd=TERRAFORM_DIR,
    )

    if result.returncode != 0:

        raise RuntimeError(
            "Terraform destroy failed."
        )

    print()
    print(
        "Terraform destroy completed."
    )


# =========================================================
# Main
# =========================================================

def main() -> int:

    print("=" * 50)
    print(" Azure Native cleanup")
    print("=" * 50)
    print()

    print("This cleanup will remove:")
    print()
    print("  - Azure ML online endpoint")
    print("  - Azure ML endpoint deployments")
    print("  - Registered model versions")
    print("  - Terraform-managed Azure resources")
    print()
    print("This is a destructive operation.")
    print()
    print(
        "Terraform backend will NOT be destroyed."
    )
    print(
        "The existing Terraform state storage remains untouched."
    )
    print()

    confirmation = input(
        "Type DESTROY to continue: "
    ).strip()

    if confirmation != "DESTROY":

        print()
        print("Cleanup cancelled.")

        return 0

    print()

    # -----------------------------------------------------
    # Check tools
    # -----------------------------------------------------

    if not azure_cli_available():

        print(
            "ERROR: Azure CLI 'az' was not found "
            "in PATH."
        )

        print()
        print("Check with:")
        print("  az --version")

        return 1

    if not terraform_available():

        print(
            "ERROR: Terraform was not found "
            "in PATH."
        )

        print()
        print("Check with:")
        print("  terraform --version")

        return 1

    # -----------------------------------------------------
    # Show tool versions
    # -----------------------------------------------------

    print("Azure CLI:")

    run_command(
        ["az", "--version"]
    )

    print()
    print("Terraform:")

    run_command(
        ["terraform", "--version"]
    )

    # -----------------------------------------------------
    # Azure ML cleanup
    # -----------------------------------------------------

    try:

        delete_endpoint()
        delete_model_versions()

    except Exception as exc:

        print()
        print(
            f"Azure cleanup failed: {exc}"
        )

        print(
            "Terraform destroy was NOT executed."
        )

        return 1

    # -----------------------------------------------------
    # Terraform cleanup
    # -----------------------------------------------------

    try:

        terraform_destroy()

    except Exception as exc:

        print()
        print(
            f"Terraform cleanup failed: {exc}"
        )

        return 1

    # -----------------------------------------------------
    # Completed
    # -----------------------------------------------------

    print()
    print("=" * 50)
    print(" Cleanup completed")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())