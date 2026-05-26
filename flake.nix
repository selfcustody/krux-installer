{
  description = "Krux-installer flake";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    let
      # -----------------------------------------------------------------------
      # ciPkgs — nixpkgs for x86_64-linux, used only by ciTest below.
      # Has no effect on devShells or any local dev workflow.
      # -----------------------------------------------------------------------
      ciPkgs = import nixpkgs {
        system = "x86_64-linux";
        config.allowUnfree = true;
      };
    in
    # -------------------------------------------------------------------------
    # devShells — for local development on Linux and macOS (nix develop).
    # This is the only entry point end users and contributors need.
    # -------------------------------------------------------------------------
    (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
          config.allowInsecure = true;
          config.allowUnsupportedSystem = true;
        };
        python = pkgs.python313;
        isLinux = pkgs.stdenv.isLinux;
        isDarwin = pkgs.stdenv.isDarwin;
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.uv
            pkgs.openssl
            pkgs.git
            pkgs.pkg-config
            pkgs.zlib
            pkgs.libffi
            pkgs.cairo
            pkgs.glib
            pkgs.gtk3
            pkgs.gobject-introspection
            pkgs.freetype
            pkgs.libusb1
            pkgs.tcl
            pkgs.tk
            pkgs.fontconfig
            pkgs.pango
            pkgs.gdk-pixbuf
            pkgs.atk
            pkgs.stdenv.cc.cc.lib
          ] ++ pkgs.lib.optionals isLinux [
            pkgs.polkit
            pkgs.libGL
            pkgs.mtdev
            pkgs.shadow
            pkgs.fontconfig
            pkgs.pango
            pkgs.gdk-pixbuf
            pkgs.atk
            pkgs.stdenv.cc.cc.lib
            pkgs.xorg.libX11
            pkgs.xorg.libXext
            pkgs.xorg.libXrender
            pkgs.xorg.libxcb
            pkgs.xorg.libXrandr
            pkgs.xorg.libXinerama
            pkgs.xorg.libXcursor
            pkgs.xorg.libXi
            pkgs.xorg.libXxf86vm
            pkgs.SDL2
            pkgs.SDL2.dev
            pkgs.SDL2_image
            pkgs.SDL2_mixer
            pkgs.SDL2_ttf
          ] ++ pkgs.lib.optionals isDarwin [
            pkgs.darwin.apple_sdk.frameworks.Cocoa
            pkgs.darwin.apple_sdk.frameworks.OpenGL
            pkgs.darwin.apple_sdk.frameworks.IOKit
            pkgs.darwin.apple_sdk.frameworks.AVFoundation
            pkgs.darwin.apple_sdk.frameworks.CoreMedia
            pkgs.darwin.apple_sdk.frameworks.CoreVideo
            pkgs.darwin.apple_sdk.frameworks.ApplicationServices
            pkgs.SDL2
            pkgs.SDL2.dev
            pkgs.SDL2_image
            pkgs.SDL2_mixer
            pkgs.SDL2_ttf
            pkgs.libcxx
          ];

          shellHook = ''
            export HOME="''${HOME:-$(pwd)/.home}"
            export XDG_DATA_HOME="$HOME/.local/share"
            export XDG_CONFIG_HOME="$HOME/.config"
            export XDG_CACHE_HOME="$HOME/.cache"

            mkdir -p "$HOME" "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"

            export UV_CACHE_DIR="$XDG_CACHE_HOME/uv"
            export UV_PYTHON_INSTALL_DIR="$XDG_DATA_HOME/uv/python"
            export UV_TOOL_DIR="$XDG_DATA_HOME/uv/tools"
            export UV_TOOL_BIN_DIR="$XDG_DATA_HOME/uv/bin"

            mkdir -p "$UV_CACHE_DIR" "$UV_PYTHON_INSTALL_DIR" "$UV_TOOL_DIR" "$UV_TOOL_BIN_DIR"

            export VIRTUAL_ENV_DISABLE_PROMPT=1
            export PIP_CACHE_DIR="$XDG_CACHE_HOME/pip"
            mkdir -p "$PIP_CACHE_DIR"

            export PATH="$UV_TOOL_BIN_DIR:$PATH"
            export UV_PYTHON="${pkgs.python313}/bin/python3"

            ${pkgs.lib.optionalString isLinux ''
              if [ -e "${pkgs.mtdev}/lib/libmtdev.so" ] && [ ! -e "${pkgs.mtdev}/lib/libmtdev.so.1" ]; then
                ln -sf "${pkgs.mtdev}/lib/libmtdev.so" "${pkgs.mtdev}/lib/libmtdev.so.1"
              fi

              export DISPLAY="''${DISPLAY:-:0}"

              export LD_LIBRARY_PATH=\
              ${pkgs.libGL}/lib:\
              ${pkgs.stdenv.cc.cc.lib}/lib:\
              ${pkgs.xorg.libX11}/lib:\
              ${pkgs.xorg.libxcb}/lib:\
              ${pkgs.mtdev}/lib:\
              ${pkgs.SDL2}/lib:\
              $LD_LIBRARY_PATH

              export PKG_CONFIG_PATH=\
              ${pkgs.SDL2}/lib/pkgconfig:\
              ${pkgs.SDL2_image}/lib/pkgconfig:\
              ${pkgs.SDL2_mixer}/lib/pkgconfig:\
              ${pkgs.SDL2_ttf}/lib/pkgconfig:\
              $PKG_CONFIG_PATH

              export CFLAGS="-I${pkgs.SDL2.dev}/include/SDL2 -I${pkgs.SDL2.dev}/include"
              export CPPFLAGS="-I${pkgs.SDL2.dev}/include/SDL2 -I${pkgs.SDL2.dev}/include"
            ''}

            ${pkgs.lib.optionalString isDarwin ''
              export SDKROOT="${pkgs.darwin.apple_sdk.MacOSX-SDK}"

              export DYLD_LIBRARY_PATH=\
              ${pkgs.SDL2}/lib:\
              ${pkgs.openssl}/lib:\
              $DYLD_LIBRARY_PATH

              export PKG_CONFIG_PATH=\
              ${pkgs.SDL2}/lib/pkgconfig:\
              ${pkgs.SDL2_image}/lib/pkgconfig:\
              ${pkgs.SDL2_mixer}/lib/pkgconfig:\
              ${pkgs.SDL2_ttf}/lib/pkgconfig:\
              $PKG_CONFIG_PATH

              export CFLAGS="-I${pkgs.SDL2.dev}/include/SDL2 -I${pkgs.SDL2.dev}/include -isysroot ${pkgs.darwin.apple_sdk.MacOSX-SDK}"
              export CPPFLAGS="-I${pkgs.SDL2.dev}/include/SDL2 -I${pkgs.SDL2.dev}/include -isysroot ${pkgs.darwin.apple_sdk.MacOSX-SDK}"
              export CXXFLAGS="-isysroot ${pkgs.darwin.apple_sdk.MacOSX-SDK}"
            ''}

            export PYTHONPATH=$PWD/src:$PYTHONPATH

            echo "Development environment setup complete!"
            echo "UV cache: $UV_CACHE_DIR"
            echo "Virtual env: .venv (managed by UV)"
            echo ""
            echo "Try running: uv sync && uv run poe dev"
            echo "you must add (users.users.<youruser>.extraGroups = [ \"dialout\" ];) in your configuration.nix, and reboot your system!!!"
          '';
        };
      }
    )) // {
      # -----------------------------------------------------------------------
      # nixosConfigurations.ciTest — CI-only NixOS VM (nix_linux.yml).
      #
      # This is a minimal NixOS machine used by GitHub Actions to run the
      # full test suite (unit + e2e + drives) inside a real NixOS environment.
      #
      # Key properties:
      #   - X server enabled so Kivy/GraphicUnitTest gets a real display
      #   - Full internet access via DHCP (needed for uv sync + firmware fetch)
      #   - Host workspace mounted at /workspace via 9p virtfs.
      #     The mount tag "workspace" is declared here via a systemd unit;
      #     the actual host path is passed at runtime by the workflow using
      #     -virtfs local,path=<workspace>,mount_tag=workspace
      #   - SSH forwarded to host port 2222 so the workflow drives test steps
      #   - Root login with a simple password — safe: ephemeral, localhost-only
      #
      # To build locally (x86_64-linux only):
      #   nix build .#nixosConfigurations.ciTest.config.system.build.vm
      # -----------------------------------------------------------------------
      nixosConfigurations.ciTest = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ({ modulesPath, ... }: {
            imports = [ "${modulesPath}/virtualisation/qemu-vm.nix" ];

            system.stateVersion = "25.05";
            nixpkgs.hostPlatform = "x86_64-linux";

            # -- VM resources tuned for GitHub Actions free runners ------------
            virtualisation = {
              cores = 2;
              memorySize = 4096;
              diskSize = 8192;

              # Forward VM SSH to host port 2222 so the workflow can ssh in.
              forwardPorts = [{
                from = "host";
                host.port = 2222;
                guest.port = 22;
              }];
            };

            # -- Workspace mount: 9p virtfs tag "workspace" -------------------
            # The host path is passed at boot time by the workflow via:
            #   -virtfs local,path=<host-path>,mount_tag=workspace,...
            # This systemd unit mounts that tag at /workspace inside the VM.
            # Load 9p kernel modules in the initrd so the virtfs mount works.
            boot.initrd.availableKernelModules = [ "9p" "9pnet_virtio" "virtio_pci" ];

            # Ensure /workspace exists as a mountpoint directory.
            systemd.tmpfiles.rules = [ "d /workspace 0755 root root -" ];

            fileSystems."/workspace" = {
              device = "workspace";
              fsType = "9p";
              options = [ "trans=virtio" "version=9p2000.L" "msize=131072" "nofail" "x-systemd.automount" ];
            };

            # -- Network: full internet access via DHCP -----------------------
            networking.useDHCP = true;
            networking.firewall.enable = false;

            # -- Display: X server so Kivy/GraphicUnitTest gets a real DISPLAY -
            services.xserver.enable = true;

            # -- SSH: root login for ephemeral CI VM only ---------------------
            services.openssh.enable = true;
            services.openssh.settings.PermitRootLogin = "yes";
            users.extraUsers.root.password = "ci";

            # -- Packages available inside the VM -----------------------------
            environment.systemPackages = with ciPkgs; [
              # nix is needed to run `nix develop` on the mounted workspace
              nix
              git
              # curl + unzip for the firmware fetch script
              curl
              unzip
            ];

            # Enable flakes inside the VM
            nix.settings.experimental-features = [ "nix-command" "flakes" ];
          })
        ];
      };
    };
}
