from skills.validation.skill import validate_logs
from skills.explanation.skill import explain_malformed_line
from skills.triage.skill import summarize_incidents

class SkillRouter:
    @staticmethod
    def route_request(action: str, payload: dict) -> dict:
        """
        Enruta la petición explícita a la skill correspondiente.
        """
        if action == "validate":
            return validate_logs(
                text=payload.get("text"),
                filepath=payload.get("filepath")
            )
        elif action == "explain":
            return explain_malformed_line(
                texto_original=payload.get("texto_original", ""),
                motivo_error=payload.get("motivo_error", ""),
                numero_linea=payload.get("numero_linea", 0)
            )
        elif action == "triage":
            return summarize_incidents(
                resumen_serializado=payload.get("resumen", {})
            )
        else:
            raise ValueError(f"Acción desconocida: {action}")
