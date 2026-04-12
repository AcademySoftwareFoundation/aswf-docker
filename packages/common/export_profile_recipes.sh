#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Pre-export all recipes referenced in the Conan profile's [replace_requires]
# section so that --build=missing can build them from source even when the
# BuildKit cache mount is empty (cache mounts don't persist between separate
# docker buildx bake invocations).

set -e

PROFILE_FILE="${ASWF_CONAN_HOME}/.conan2/profiles_${ASWF_PKG_ORG}/${ASWF_CONAN_CHANNEL}"
RECIPES_DIR="${ASWF_CONAN_HOME}/recipes"

if [ ! -f "${PROFILE_FILE}" ]; then
    echo "Profile ${PROFILE_FILE} not found, skipping recipe pre-export"
    exit 0
fi

# Also process included profiles (e.g. "include(ci_common6)")
PROFILES="${PROFILE_FILE}"
INCLUDED=$(grep '^include(' "${PROFILE_FILE}" | sed 's/include(\(.*\))/\1/')
for inc in ${INCLUDED}; do
    inc_file="${ASWF_CONAN_HOME}/.conan2/profiles_${ASWF_PKG_ORG}/${inc}"
    if [ -f "${inc_file}" ]; then
        PROFILES="${PROFILES} ${inc_file}"
    fi
done

# Parse [replace_requires] entries from all profiles
# Format: "name/*: name/version@user/channel"
for profile in ${PROFILES}; do
    grep -E '^[a-z].*: [a-z].*/.*@' "${profile}" 2>/dev/null || true
done | sort -u | while IFS=': ' read -r _pattern ref; do
    # Skip entries without a proper reference
    [ -z "${ref}" ] && continue

    # Parse name/version@user/channel
    name_version="${ref%%@*}"
    user_channel="${ref#*@}"
    name="${name_version%%/*}"
    version="${name_version#*/}"
    user="${user_channel%%/*}"
    channel="${user_channel#*/}"

    # Skip if recipe directory doesn't exist
    recipe_dir="${RECIPES_DIR}/${name}"
    [ ! -d "${recipe_dir}" ] && continue

    # Determine recipe subfolder from config.yml if present
    config_yml="${recipe_dir}/config.yml"
    if [ -f "${config_yml}" ]; then
        subfolder=$(yq ".versions[\"${version}\"].folder" "${config_yml}" 2>/dev/null)
        if [ -n "${subfolder}" ] && [ "${subfolder}" != "null" ]; then
            recipe_dir="${recipe_dir}/${subfolder}"
        fi
    fi

    [ ! -f "${recipe_dir}/conanfile.py" ] && continue

    # Export the recipe to the Conan cache
    echo "Pre-exporting ${name}/${version}@${user}/${channel}"
    conan export \
        --name "${name}" \
        --version "${version}" \
        --user "${user}" \
        --channel "${channel}" \
        "${recipe_dir}" 2>/dev/null || true
done

echo "Recipe pre-export complete"
