from flask import Blueprint, jsonify, request

from .actions_bus import dispatch, list_actions

actions_bp = Blueprint("actions_api", __name__)


@actions_bp.route("/api / actions", methods=["GET"])
def api_actions():
    return jsonify({"actions": list_actions(), "count": len(list_actions())})


@actions_bp.route("/api / action/<agent>/<path:action>", methods=["POST"])
def api_action_dispatch(agent, action):
    try:
        payload: request.get_json(silent=True) or {}
        out = dispatch(agent, action, payload)
        return jsonify({"ok": True, "result": out}), 200
    except KeyError as e:
        return jsonify({"ok": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
