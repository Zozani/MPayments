#!/bin/bash

# Nom de l'application
APP_NAME="Payments"
VERSION="1.0.0"
BUNDLE_IDENTIFIER="com.fgs.payments"

# Dossier contenant l'application
DIST_DIR="dist"
APP_DIR="${DIST_DIR}/${APP_NAME}.app"
INSTALLER_="${DIST_DIR}/${APP_NAME}.app"


# Créer le fichier .pkg
pkgbuild --root "${APP_DIR}" --identifier "${BUNDLE_IDENTIFIER}" --version "${VERSION}" --install-location "/Applications/MPayments.app" "${DIST_DIR}/${APP_NAME} Installer.pkg"

echo "Fichier .pkg créé avec succès : ${DIST_DIR}/${APP_NAME}Installer.pkg"