# GitHub NVDA add-on (starter scaffold)

This repository contains an NVDA add-on that improves accessibility for the
GitHub Desktop (Electron) application. The initial scaffold provides a small
appModule that announces repository and view context when focus changes and
includes a developer logging mode to inspect the UI tree.

Installation (local testing)

1. Clone this repository and ensure the directory structure is preserved (manifest.ini at the repo root and the package files). Example:

   git clone https://github.com/voyager2264/github-add-on.git

2. Build a local add-on package (zip the add-on files and rename to .nvda-addon):

   From the repository root:
   zip -r github-0.1.0.zip manifest.ini appModules README.md LICENSE
   mv github-0.1.0.zip github-0.1.0.nvda-addon

3. On the Windows test machine with NVDA installed, double-click the .nvda-addon file or open NVDA > Tools > Add-ons > Install and select the file. Restart NVDA when prompted.

4. Open GitHub Desktop and move focus around; with developer mode disabled the add-on will attempt lightweight announcements for repository and view. To enable developer logging, set the add-on config `developerMode` to True using NVDA's Add-on configuration UI (this scaffold stores a config value but a full settings UI will be added in future iterations).

Packaging for release

- The NVDA add-on is the zipped add-on folder renamed with a .nvda-addon extension. For releases we will create a GitHub Release and attach the .nvda-addon file and screenshots.

Publishing to the NVDA add-on site

1. Create an account at https://addons.nvda-project.org/ and sign in.
2. Create a new add-on entry and upload the .nvda-addon, provide the summary, full description (this README), screenshots, and select the MIT license.
3. For future releases: tag a release in GitHub, attach the .nvda-addon and update the change log.

License

This project is provided under the MIT License (see LICENSE).
