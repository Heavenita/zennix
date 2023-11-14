def gerar(template, propiedades, valores):
    for propiedade in propiedades:
            if propiedade == "gerencia":
                template.append(f"/ip address add address={valores['gerencia']} interface=ether5 network={valores['gerencia_network']}")
            if propiedade == "valido":
                template.append(f"/ip address add address={valores['valido']} interface=br_NET network={valores['valido']}")
            if propiedade == "interna":
                template.append(f"/ip address add address={valores['interna']} interface=ether1 network={valores['interna_network']}")
            if propiedade == "queue":
                template.append(f"/queue simple add max-limit={valores['queue']}M/{valores['queue']}M name=queue1 target={valores['interna_network']}")
            if propiedade == "rota":
                template.append(f"/ip route add distance=1 gateway={valores['route']}")
            if propiedade == "snmp":
                template.append(f"/snmp set contact=\"Tec System\" enabled=yes location=\"{valores['location']}\"")
            if propiedade == "nomenclatura":
                template.append(f"/system identity set name={valores['nomenclatura']}")
    return template

def verificar_propiedade(propiedades):
    display_propiedades = []
    if "gerencia" in propiedades:
        display_propiedades.append("<b> IP Gerencia </b> <br> <br>")
        display_propiedades.append("Gerencia: <input type='text' class='ipv4-input' name='gerencia' placeholder='Gerencia' required><br><br>")
        display_propiedades.append("Gerencia Network: <input type='text' class='ipv4-input' name='gerencia_network' placeholder='Gerencia Network' required><br><br>")
        display_propiedades.append("Gerencia Barramento: <input type='number' name='gerencia_barramento' placeholder='Gerencia Barramento' min='0' max='32' required><br><br>")
    if "valido" in propiedades:
        display_propiedades.append("<b> IP Válido </b> <br> <br>")
        display_propiedades.append("Valido: <input type='text' class='ipv4-input' name='valido' placeholder='Valido' required><br><br>")
    if "nomenclatura" in propiedades:
        display_propiedades.append("<b> Nomenclatura </b> <br> <br>")
        display_propiedades.append("Nomenclatura: <input type='text' name='nomenclatura' placeholder='Nomenclatura' required><br><br>")
    if "queue" in propiedades:
        display_propiedades.append("<b>Velocidade de banda:</b> <br> <br>")
        display_propiedades.append("Queue: <input type='number' name='queue' placeholder='Queue' min='0' required><br><br>")
        display_propiedades.append("Target rede interna: <input type='text' class='ipv4-input' name='interna_network' placeholder='Target' required><br><br>")
        display_propiedades.append("Target barramento: <input type='number' name='queue_barramento' placeholder='Target barramento' min='0' max='32' required><br><br>")
    return display_propiedades

def concatenar(valor1, valor2):
    valor1 = str(valor1)
    valor2 = str(valor2)
    return valor1 + "/" + valor2