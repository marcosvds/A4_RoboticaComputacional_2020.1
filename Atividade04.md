# Robótica Computacional - Atividade 1 do projeto

Atenção: o grupo de 3 pessoas desta atividade deve se manter fixo até a entrega do projeto. Você **pode trocar** o grupo com que fez atividades anteriores. 



No ROS a OpenCV trabalha com base em eventos. Esta atividade permite que você estude isso mais a fundo


### 1. Programa ROS 

Primeiro rode o programa que centraliza o robô numa caixa vermelha. Crie um objeto vermelho no Gazebo para testar o código.

Faça um clone de [https://github.com/insper/robot20/](https://github.com/insper/robot20/) **dentro** de sua pasta `catkin_ws/src`.

    cd ~/catkin_ws/src
    git clone https://github.com/insper/robot20/

Lembre-se de **sempre** executar o `catkin_make` depois de criar novos arquivos `*.py`

    cd ~/catkin_ws
    catkin_make


Estude o código de `cor.py`. Você pode começar executando este programa.

Lembre-se de que você vai precisar estar conectado a algum robô simulado para poder testar, como o [my simulation ](https://github.com/.arnaldojr/my_simulation).


Rode num terminal o comando para que o tópico de câmera tenha um repetidor (relay) chamado `/kamera`

    rosrun topic_tools relay  /camera/rgb/image_raw/compressed /kamera

E em outro terminal

    rosrun exemplos_python cor.py

Se necessário, **crie uma caixa vermelha** usando a interface do Gazebo.


**Agora, faça:**

![](creepers.jpg)

Modique este programa para que o robô centralize num creeper **azul** ou **verde**:

Depois de centralizar, usando a informação do *laser* (tópico `\scan`) faça o robô se aproximar do *creeper* e tocá-lo gentilmente.  Isso vai ser base para depois incluirmos o comando da garra do robô. 

Você deve testar com o robô a cerca de $1.75 m$ do creeper.


Crie [seu próprio projeto](https://github.com/Insper/robot20/blob/master/guides/projeto_rospython.md), não trabalhe na pasta clonada do professor.


