Vagrant.configure("2") do |config|

  # Set vagrant box
  config.vm.box = "ubuntu/focal64"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.20"

  # Virtual machine config
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = "4"
  end

  # Provisioning
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt update
    sudo apt install openjdk-11-jdk -y

    sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
      https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
    echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
      https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
      /etc/apt/sources.list.d/jenkins.list > /dev/null
    sudo apt-get update
    sudo apt-get install jenkins -y

  SHELL
end
