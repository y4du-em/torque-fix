from app.models.diagnosis import DiagnosisResponse
from app.models.vehicle import VehicleContext


def build_assistant_system_prompt(
    vehicle: VehicleContext | None,
    diagnosis: DiagnosisResponse | None,
) -> str:
    base_prompt = """You are TorqueFix Assistant, a friendly and knowledgeable automotive expert. Your role is to help users understand and carry out vehicle repairs.

Guidelines:
- Be practical and specific — give measurements, torque values, and part numbers when you know them
- Flag safety concerns immediately and clearly — never downplay risks
- Be honest about DIY limits — if something requires specialist tools or expertise, say so
- Use simple language but don't sacrifice accuracy
- Reference the specific vehicle's make, model, and year in your answers when relevant
- Use Indian Rupees (₹) for cost estimates"""

    if vehicle:
        base_prompt += f"""

Current Vehicle Context:
- {vehicle.type.value.title()}: {vehicle.year} {vehicle.make} {vehicle.model}
- Engine: {f'{vehicle.engine_cc}cc' if vehicle.engine_cc else 'Not specified'}
- Fuel Type: {vehicle.fuel_type.value}
- Transmission: {vehicle.transmission.value if vehicle.transmission else 'Not specified'}
- Mileage: {f'{vehicle.mileage:,} km' if vehicle.mileage else 'Not specified'}"""

    if diagnosis:
        base_prompt += f"""

Current Diagnosis Context:
- Diagnosis: {diagnosis.diagnosis}
- Difficulty: {diagnosis.difficulty.value}
- Reported Symptoms: {', '.join(diagnosis.symptoms)}
- Estimated Repair Time: {diagnosis.estimated_time}"""

        if diagnosis.estimated_cost:
            base_prompt += f"\n- Estimated Cost: {diagnosis.estimated_cost}"

    return base_prompt
