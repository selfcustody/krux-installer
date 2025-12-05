{
  description = "Krux-installer flake";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
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
            pkgs.SDL2_image
            pkgs.SDL2_mixer
            pkgs.SDL2_ttf
          ] ++ pkgs.lib.optionals isDarwin [
            pkgs.darwin.apple_sdk.frameworks.Cocoa
            pkgs.darwin.apple_sdk.frameworks.OpenGL
            pkgs.darwin.apple_sdk.frameworks.IOKit
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

            ${pkgs.lib.optionalString isLinux ''
              if [ -e "${pkgs.mtdev}/lib/libmtdev.so" ] && [ ! -e "${pkgs.mtdev}/lib/libmtdev.so.1" ]; then
                ln -sf "${pkgs.mtdev}/lib/libmtdev.so" "${pkgs.mtdev}/lib/libmtdev.so.1"
              fi

              export LD_LIBRARY_PATH=\
              ${pkgs.libGL}/lib:\
              ${pkgs.stdenv.cc.cc.lib}/lib:\
              ${pkgs.xorg.libX11}/lib:\
              ${pkgs.xorg.libxcb}/lib:\
              ${pkgs.mtdev}/lib:\
              ${pkgs.SDL2}/lib:\
              $LD_LIBRARY_PATH
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
    );
}