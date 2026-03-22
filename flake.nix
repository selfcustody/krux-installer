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
        python = pkgs.python314;
        isLinux = pkgs.stdenv.isLinux;
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.poetry
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
          ];

          shellHook = ''
            export HOME="''${HOME:-$(pwd)/.home}"
            export XDG_DATA_HOME="$HOME/.local/share"
            export XDG_CONFIG_HOME="$HOME/.config"
            export XDG_CACHE_HOME="$HOME/.cache"

            mkdir -p "$HOME" "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"

            export POETRY_CACHE_DIR="$XDG_CACHE_HOME/pypoetry"
            export POETRY_DATA_DIR="$XDG_DATA_HOME/pypoetry"
            export POETRY_CONFIG_DIR="$XDG_CONFIG_HOME/pypoetry"
            export POETRY_VENV_PATH="$POETRY_CACHE_DIR/virtualenvs"

            mkdir -p "$POETRY_CACHE_DIR" "$POETRY_DATA_DIR" "$POETRY_CONFIG_DIR" "$POETRY_VENV_PATH"

            export VIRTUAL_ENV_DISABLE_PROMPT=1
            export PIP_CACHE_DIR="$XDG_CACHE_HOME/pip"
            mkdir -p "$PIP_CACHE_DIR"

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
              $LD_LIBRARY_PATH
            ''}

            export PYTHONPATH=$PWD/src:$PYTHONPATH

            poetry config virtualenvs.in-project false
            poetry config virtualenvs.path "$POETRY_VENV_PATH"
            poetry config cache-dir "$POETRY_CACHE_DIR"

            echo "Development environment setup complete!"
            echo "Poetry cache: $POETRY_CACHE_DIR"
            echo "Virtual envs: $POETRY_VENV_PATH"
            echo ""
            echo "Try running: poetry install && poetry run poe dev"
            echo "you must add (users.users.<youruser>.extraGroups = [ \"dialout\" ];) in your configuration.nix, and reboot your system!!!"
          '';
        };
      }
    );
}