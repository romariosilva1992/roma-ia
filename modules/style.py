class StyleManager:
    def __init__(self):
        self.default_style = {
            "tone": "Analítico e envolvente",
            "pov": "Terceira pessoa",
            "sentence_length": "Média a curta",
            "metaphors_usage": "Moderada",
        }

    def get_style_prompt(self, custom_style: dict | None = None) -> str:
        style = {**self.default_style, **(custom_style or {})}
        return "\n".join(
            [
                "[DIRETRIZES DE ESTILO DA ROMA]",
                f"- Tom de Voz: {style['tone']}",
                f"- Ponto de Vista (POV): {style['pov']}",
                f"- Ritmo das Frases: {style['sentence_length']}",
                f"- Uso de Metáforas: {style['metaphors_usage']}",
                "Mantenha esta identidade em todo o conteúdo gerado.",
            ]
        )