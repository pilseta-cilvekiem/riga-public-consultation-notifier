#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(realpath "$(dirname "${BASH_SOURCE[0]}")/..")"
ENV_FILE="${REPOSITORY_ROOT}/.env"
SECRETS_DIRECTORY="${REPOSITORY_ROOT}/secrets"

mkdir -p "$(dirname "${ENV_FILE}")"
touch "${ENV_FILE}"
install -d -m 700 "${SECRETS_DIRECTORY}"

extract_env_value() {
	local variable_name="$1"
	local variable_value
	variable_value="$({ grep -E "^[[:space:]]*${variable_name}=" "${ENV_FILE}" || true; } | tail -n 1 | cut -d "=" -f 2-)"
	variable_value="${variable_value#\"}"
	variable_value="${variable_value%\"}"
	variable_value="${variable_value#\'}"
	variable_value="${variable_value%\'}"
	echo "${variable_value}"
}

upsert_env_value() {
	local variable_name="$1"
	local variable_value="$2"

	if grep -qE "^[[:space:]]*${variable_name}=" "${ENV_FILE}"; then
		sed -i "s|^[[:space:]]*${variable_name}=.*$|${variable_name}=${variable_value}|" "${ENV_FILE}"
	else
		printf "%s=%s\n" "${variable_name}" "${variable_value}" >> "${ENV_FILE}"
	fi
}

slack_bot_user_oauth_token_file="$(extract_env_value "SLACK_BOT_USER_OAUTH_TOKEN_FILE")"
if [[ -z "${slack_bot_user_oauth_token_file}" ]]; then
	default_slack_bot_user_oauth_token_file="${SECRETS_DIRECTORY}/slack_bot_user_oauth_token"
	upsert_env_value "SLACK_BOT_USER_OAUTH_TOKEN_FILE" "${default_slack_bot_user_oauth_token_file}"
	slack_bot_user_oauth_token_file="${default_slack_bot_user_oauth_token_file}"
fi

if [[ -e "${slack_bot_user_oauth_token_file}" && ! -f "${slack_bot_user_oauth_token_file}" ]]; then
	echo "SLACK_BOT_USER_OAUTH_TOKEN_FILE must point to a file: ${slack_bot_user_oauth_token_file}"
	exit 1
fi

if [[ ! -f "${slack_bot_user_oauth_token_file}" ]]; then
	if [[ ! -t 0 ]]; then
		echo "SLACK_BOT_USER_OAUTH_TOKEN_FILE points to a missing file (${slack_bot_user_oauth_token_file}) and interactive input is not available."
		exit 1
	fi

	mkdir -p "$(dirname "${slack_bot_user_oauth_token_file}")"
	slack_bot_user_oauth_token=""
	while [[ -z "${slack_bot_user_oauth_token}" ]]; do
		read -r -s -p "Enter Slack Bot User OAuth Token: " slack_bot_user_oauth_token
		echo
	done

	install -m 600 /dev/null "${slack_bot_user_oauth_token_file}"
	printf "%s\n" "${slack_bot_user_oauth_token}" > "${slack_bot_user_oauth_token_file}"
fi

slack_channel_id="$(extract_env_value "SLACK_CHANNEL_ID")"
if [[ -z "${slack_channel_id}" ]]; then
	if [[ ! -t 0 ]]; then
		echo "SLACK_CHANNEL_ID is missing in ${ENV_FILE} and interactive input is not available."
		exit 1
	fi

	while [[ -z "${slack_channel_id}" ]]; do
		read -r -p "Enter SLACK_CHANNEL_ID: " slack_channel_id
	done

	upsert_env_value "SLACK_CHANNEL_ID" "${slack_channel_id}"
fi

set -a
# shellcheck source=/dev/null
source "${ENV_FILE}"
set +a

PYTHONPATH="${REPOSITORY_ROOT}" python3 -m src
