Vagrant.require_version ">= 2.0.2"

$post_msg = <<MSG
-----------------------------------------------------
URLS:
 - Zuul dashboard  - http://10.10.10.5/
 - Zuul status     - http://10.10.10.5/status.json
 - Gerrit          - http://10.10.10.5:8080/
-----------------------------------------------------
MSG

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.provider "virtualbox" do |vbox|
    vbox.memory = 4096
    vbox.cpus = 2
    vbox.gui = false
  end

  # Disable the new default behavior introduced in Vagrant 1.7, to
  # ensure that all Vagrant machines will use the same SSH key pair.
  # See https://github.com/mitchellh/vagrant/issues/5005
  config.ssh.insert_key = false
  config.vm.network "private_network", ip: "10.10.10.5"

  config.vm.synced_folder ".", "/opt/app", owner: "vagrant", group: "vagrant", create: true

  config.vm.provision "ansible" do |ansible|
    ansible.compatibility_mode = "2.0"
    ansible.verbose = "vv"
    ansible.playbook = "playbooks/vagrant-dev.yml"
  end

  config.vm.post_up_message = $post_msg
end
