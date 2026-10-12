"""
NVDA appModule for GitHub Desktop (starter scaffold).
Place this file in the add-on's appModules/ directory.

This module is intentionally small: it announces repository and view changes
when focus moves, and has a developer logging mode to help map the UI tree.

Further work will add explicit selectors for file lists, diff panes and
keyboard commands to navigate them.
"""

import appModule
import api
import speech
import addonHandler

log = api.getLogger("github.appModule")

class AppModule(appModule.AppModule):
    """Basic appModule for GitHub Desktop (Electron).

    NVDA will load this module for the GitHub Desktop process/window class.
    """

    def event_gainFocus(self, obj, nextHandler):
        """Called when focus moves within the target application.
        We attempt to announce repository and current view information.
        """
        try:
            repo = self._get_repository_name(obj)
            view = self._get_current_view(obj)
            messages = []
            if repo:
                messages.append("Repository: {}".format(repo))
            if view:
                messages.append("View: {}".format(view))
            if messages:
                # Use NVDA speech API to announce the message succinctly
                speech.speakMessage(" — ".join(messages))

            # Developer logging for tree inspection
            try:
                developer_mode = addonHandler.getConfig("developerMode", False)
            except Exception:
                developer_mode = False
            if developer_mode:
                try:
                    log.debug("Focused object: %s; role=%s; controlType=%s",
                              getattr(obj, "name", None), getattr(obj, "roleName", None), getattr(obj, "controlType", None))
                    children = []
                    for i, c in enumerate(getattr(obj, "children", [])[:8]):
                        try:
                            children.append((i, getattr(c, "name", ""), getattr(c, "roleName", "")))
                        except Exception:
                            children.append((i, "<unreadable>", ""))
                    log.debug("Children sample: %s", children)
                except Exception:
                    log.debug("Failed to dump focused object's children")
        finally:
            # Always call the next handler
            nextHandler()

    def _get_repository_name(self, obj):
        """Heuristic walk up the object tree to find a likely repository title.

        This is a conservative heuristic: it looks for short title-like labels
        or things that contain a slash (owner/repo).
        """
        try:
            cur = obj
            depth = 0
            while cur and depth < 12:
                name = getattr(cur, "name", None) or ""
                role = getattr(cur, "roleName", "") or ""
                # common pattern: repository names often contain a slash
                if "/" in name and len(name) < 80:
                    return name.strip()
                # title bar or heading labels may contain the repo name
                if role and role.lower() in ("title bar", "label", "heading"):
                    if name and len(name) < 100:
                        return name.strip()
                cur = getattr(cur, "parent", None)
                depth += 1
        except Exception:
            log.debug("_get_repository_name failed", exc_info=True)
        return None

    def _get_current_view(self, obj):
        """Detect main view names like Changes, History, Branches.

        Walk upward and look for short headings that match expected view names.
        """
        view_names = {"changes", "history", "branches", "repository", "pull requests", "pull requests"}
        try:
            cur = obj
            depth = 0
            while cur and depth < 12:
                name = (getattr(cur, "name", "") or "").strip()
                if name and name.lower() in view_names:
                    return name
                cur = getattr(cur, "parent", None)
                depth += 1
        except Exception:
            log.debug("_get_current_view failed", exc_info=True)
        return None
