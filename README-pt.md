# Dispositivo de Coleta de Tempo de Reação

Este é um projeto de um dispositivo de coleta de tempo de reação simples e de escolha,
que utiliza estímulos visuais, sonoros e auditivos. O projeto é baseado na biblioteca
microPython e é projetado para funcionar com o microcontrolador ESP32.

Para ler está página em inglês, [clique aqui](https://github.com/BrunoFurlanetto/collection_device/blob/main/README.md).

## Funcionalidades

O dispositivo de coleta de tempo de reação permite medir o tempo de reação de um
usuário em resposta a diferentes estímulos. Ele fornece três tipos de estímulos: 
visual, sonoro e auditivo. O usuário deve reagir o mais rápido possível
quando o estímulo é apresentado e o dispositivo registra o tempo de reação.

## Pré-requisitos

- Microcontrolador ESP32
- Conexão com o computador para programação
- Ambiente Python com microPython instalado
- Acesso à internet para baixar dependências

## Instalação

1. Clone este repositório em sua máquina local:

   ```
   git clone https://github.com/BrunoFurlanetto/collection_device.git
   ```

2. Acesse o diretório do projeto:

   ```
   cd dispositivo-coleta-tempo-reacao
   ```

3. Crie um ambiente virtual utilizando a ferramenta `venv`:

   ```
   python -m venv venv
   ```

4. Ative o ambiente virtual:

    - No Windows:

      ```
      venv\Scripts\activate.bat
      ```

    - No Linux/macOS:

      ```
      source venv/bin/activate
      ```

5. Instale as dependências do projeto:

   ```
   pip install -r requirements.txt
   ```

6. Limpe o flash do ESP32:

    - Conecte o ESP32 ao computador via USB. Se certifique que o cabo USB também tenha
       capacidade de transmissão de dads.
    - Abra um terminal e execute o seguinte comando:

      ```
      esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
      ```

      **Observação:** Substitua `/dev/ttyUSB0` pelo caminho adequado da porta serial 
      do ESP32 no seu sistema.

## Uso

1. Conecte o ESP32 ao computador via USB.

2. Certifique-se de que o ambiente virtual esteja ativado:

    - No Windows:

      ```
      venv\Scripts\activate.bat
      ```

    - No Linux/macOS:

      ```
      source venv/bin/activate
      ```

3. Execute o programa principal e forneça a porta de comunicação com o ESP32:

   ```
   python main.py
   ```

4. Siga as instruções no terminal para interagir com o dispositivo de coleta de tempo 
   de reação.

5. Para fazer se obter os arquivos de saída dos testes execute o arquivo `get_file.bat`
    para o windowns e `get_file.sh` no linux. Forneça então o nome que deseja para os 
    arquivos.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
