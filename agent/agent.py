import asyncio
import snmp_agent
import requests

def get_system_data():
    try:
        url = "http://localhost:8085/data.json"
        response = requests.get(url)
        data = response.json()

        def find_value_in_section(children, section_name, target_text):
            for item in children:
                if item.get("Text") == section_name and "Children" in item:
                    for child in item["Children"]:
                        if child.get("Text") == target_text:
                            return child.get("Value")
                if "Children" in item and item["Children"]:
                    result = find_value_in_section(item["Children"], section_name, target_text)
                    if result:
                        return result
            return None

        # CPU Metrics
        temperature_cpu = find_value_in_section(data["Children"], "Temperatures", "CPU Package")
        temperature_cpu_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', temperature_cpu))) if temperature_cpu else None

        power_cpu = find_value_in_section(data["Children"], "Powers", "CPU Package")
        power_cpu_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', power_cpu))) if power_cpu else None

        cpu_load = find_value_in_section(data["Children"], "Load", "CPU Total")
        cpu_load_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', cpu_load))) if cpu_load else None

        # Memory Metrics
        memory_load = find_value_in_section(data["Children"], "Load", "Memory")
        memory_load_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', memory_load))) if memory_load else None

        # GPU Metrics
        gpu_temp = find_value_in_section(data["Children"], "Temperatures", "GPU Core")
        gpu_temp_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', gpu_temp))) if gpu_temp else None

        gpu_power = find_value_in_section(data["Children"], "Powers", "GPU Power")
        gpu_power_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', gpu_power))) if gpu_power else None

        # Disk Metrics
        disk_used = find_value_in_section(data["Children"], "Load", "Used Space")
        disk_used_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', disk_used))) if disk_used else None

        print("Temperatura CPU (ºC):", temperature_cpu)
        print("Potencia CPU (W):", power_cpu)
        print("Carga CPU (%):", cpu_load)
        print("Uso de Memoria (%):", memory_load)
        print("Temperatura GPU (ºC):", gpu_temp)
        print("Potencia GPU (W):", gpu_power)
        print("Espacio Disco Usado (%):", disk_used)
        print("\n\n")

        return (
            temperature_cpu_value,
            power_cpu_value,
            cpu_load_value,
            memory_load_value,
            gpu_temp_value,
            gpu_power_value,
            disk_used_value
        )

    except Exception as e:
        print("Error:", e)
        return (None, None, None, None, None, None, None)

# personalized MIB
async def handler(req: snmp_agent.SNMPRequest) -> snmp_agent.SNMPResponse:
    (temp_cpu, power_cpu, load_cpu, load_mem, temp_gpu, power_gpu, disk_used) = get_system_data()
    
    vbs = [
        snmp_agent.VariableBinding('1.3.6.1.4.1.12345.1.0', snmp_agent.Integer(int(temp_cpu) if temp_cpu is not None else -1)),
        snmp_agent.VariableBinding('1.3.6.1.4.1.12345.1.1', snmp_agent.Integer(int(power_cpu) if power_cpu is not None else -1)),
        snmp_agent.VariableBinding('1.3.6.1.4.1.12345.1.2', snmp_agent.Integer(int(load_cpu) if load_cpu is not None else -1)),
        snmp_agent.VariableBinding('1.3.6.1.4.1.12345.1.3', snmp_agent.Integer(int(load_mem) if load_mem is not None else -1)),
        snmp_agent.VariableBinding('1.3.6.1.4.1.12345.1.4', snmp_agent.Integer(int(temp_gpu) if temp_gpu is not None else -1)),
        snmp_agent.VariableBinding('1.3.6.1.4.1.12345.1.5', snmp_agent.Integer(int(power_gpu) if power_gpu is not None else -1)),
        snmp_agent.VariableBinding('1.3.6.1.4.1.12345.1.6', snmp_agent.Integer(int(disk_used) if disk_used is not None else -1)),
    ]
    
    res_vbs = snmp_agent.utils.handle_request(req=req, vbs=vbs)
    res = req.create_response(res_vbs)
    return res

async def main():
    sv = snmp_agent.Server(handler=handler, host='0.0.0.0', port=162)
    await sv.start()
    print("Servidor SNMP escuchando en 0.0.0.0:162")


    while True:
        await asyncio.sleep(3600)

asyncio.run(main())