#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENVS_DIR="${ROOT}/peer_envs"

BIOMNI_REPO_DEFAULT="/lab_workspace/projects/Biomni-main"
STELLA_REQ_DEFAULT="/lab_workspace/projects/RBioBench/agents_run/stella/STELLA/requirements.txt"

RENZO_PY_DEFAULT="${ROOT}/.venv312/bin/python"
if [[ -x "${RENZO_PY_DEFAULT}" ]]; then
  PYTHON_BIN_DEFAULT="${RENZO_PY_DEFAULT}"
else
  PYTHON_BIN_DEFAULT="python3"
fi

PYTHON_BIN="${PYTHON_BIN:-$PYTHON_BIN_DEFAULT}"
BIOMNI_REPO_DIR="${BIOMNI_REPO_DIR:-$BIOMNI_REPO_DEFAULT}"
STELLA_REQ_FILE="${STELLA_REQ_FILE:-$STELLA_REQ_DEFAULT}"
RENZO_REQ_FILE="${RENZO_REQ_FILE:-${ROOT}/backend/requirements.txt}"

mkdir -p "${ENVS_DIR}"

create_env() {
  local name="$1"
  local env_dir="${ENVS_DIR}/${name}"
  if [[ -x "${env_dir}/bin/python" ]]; then
    echo "[peer-env] ${name}: exists (${env_dir})"
    return 0
  fi
  echo "[peer-env] ${name}: creating venv (${env_dir})"
  "${PYTHON_BIN}" -m venv "${env_dir}"
  "${env_dir}/bin/python" -m pip install --upgrade pip wheel setuptools
  if [[ -f "${RENZO_REQ_FILE}" ]]; then
    echo "[peer-env] ${name}: installing base deps from ${RENZO_REQ_FILE}"
    "${env_dir}/bin/python" -m pip install -r "${RENZO_REQ_FILE}"
  fi
}

create_env biomni
echo "[peer-env] biomni: installing from ${BIOMNI_REPO_DIR}"
if [[ ! -f "${BIOMNI_REPO_DIR}/pyproject.toml" ]]; then
  echo "[peer-env] biomni: ERROR: BIOMNI_REPO_DIR not found: ${BIOMNI_REPO_DIR}" >&2
  exit 2
fi
"${ENVS_DIR}/biomni/bin/python" -m pip install -e "${BIOMNI_REPO_DIR}"

create_env stella
echo "[peer-env] stella: installing requirements from ${STELLA_REQ_FILE}"
if [[ ! -f "${STELLA_REQ_FILE}" ]]; then
  echo "[peer-env] stella: ERROR: STELLA_REQ_FILE not found: ${STELLA_REQ_FILE}" >&2
  exit 2
fi
"${ENVS_DIR}/stella/bin/python" -m pip install -r "${STELLA_REQ_FILE}"

create_env tooluniverse
echo "[peer-env] tooluniverse: installing official package"
"${ENVS_DIR}/tooluniverse/bin/python" -m pip install tooluniverse

echo "[peer-env] done"
echo "biomni python: ${ENVS_DIR}/biomni/bin/python"
echo "stella python: ${ENVS_DIR}/stella/bin/python"
echo "tooluniverse python: ${ENVS_DIR}/tooluniverse/bin/python"
