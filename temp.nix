{ config, pkgs, ... }:

{
  imports = [ ./hardware-configuration.nix ];

  # Bootloader (most common)
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  # Networking
  networking.networkmanager.enable = true;
  networking.hostName = "thinkpad"; # pick your hostname

  # Locale & keyboard
  time.timeZone = "Europe/Oslo";
  i18n.defaultLocale = "en_US.UTF-8";

  services.xserver.enable = true;
  services.xserver.layout = "no"; # Norwegian layout
  services.xserver.xkb.variant = "";

  # Display manager + i3 WM
  services.xserver.displayManager.lightdm.enable = true;
  services.xserver.windowManager.i3.enable = true;

  # Sound
  sound.enable = true;
  hardware.pulseaudio.enable = true;

  # OpenGL (graphics accel)
  hardware.opengl.enable = true;

  # Basic users
  users.users.yourname = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" ]; # sudo + network
    packages = with pkgs; [ firefox git neovim tmux ];
  };

  # Allow unfree (needed for some firmware/software)
  nixpkgs.config.allowUnfree = true;

  # Enable ssh if you want remote access
  services.openssh.enable = true;

  # System packages (root level)
  environment.systemPackages = with pkgs; [ vim ];

  # Auto upgrade nixpkgs channels (optional)
  system.autoUpgrade.enable = true;
}
