{
   description = "Krux-installer flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python314;
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.poetry  
            pkgs.polkit
            pkgs.openssl
            #pkgs.uv
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
            pkgs.xorg.libX11
            pkgs.xorg.libXext
            pkgs.xorg.libXrender
            pkgs.xorg.libxcb
            pkgs.libGL           
            pkgs.stdenv.cc.cc.lib 
            pkgs.mtdev 
            pkgs.shadow
            pkgs.xorg.libXrandr
            pkgs.xorg.libXinerama
            pkgs.xorg.libXcursor
            pkgs.xorg.libXi
            pkgs.xorg.libXxf86vm
            pkgs.fontconfig
            pkgs.pango
            pkgs.gdk-pixbuf
            pkgs.atk
          ];
          shellHook = ''
            # Set up proper directories for Poetry and Python
            export HOME="''${HOME:-$(pwd)/.home}"
            export XDG_DATA_HOME="$HOME/.local/share"
            export XDG_CONFIG_HOME="$HOME/.config" 
            export XDG_CACHE_HOME="$HOME/.cache"
            
            # Create necessary directories
            mkdir -p "$HOME" "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
            
            # Poetry configuration
            export POETRY_CACHE_DIR="$XDG_CACHE_HOME/pypoetry"
            export POETRY_DATA_DIR="$XDG_DATA_HOME/pypoetry"
            export POETRY_CONFIG_DIR="$XDG_CONFIG_HOME/pypoetry"
            export POETRY_VENV_PATH="$POETRY_CACHE_DIR/virtualenvs"
            
            # Create Poetry directories
            mkdir -p "$POETRY_CACHE_DIR" "$POETRY_DATA_DIR" "$POETRY_CONFIG_DIR" "$POETRY_VENV_PATH"
            
            # Python and virtual environment setup
            export VIRTUAL_ENV_DISABLE_PROMPT=1
            export PIP_CACHE_DIR="$XDG_CACHE_HOME/pip"
            mkdir -p "$PIP_CACHE_DIR"
            
            # Make sure Kivy finds mtdev
            if [ -e "${pkgs.mtdev}/lib/libmtdev.so" ] && [ ! -e "${pkgs.mtdev}/lib/libmtdev.so.1" ]; then
              ln -sf "${pkgs.mtdev}/lib/libmtdev.so" "${pkgs.mtdev}/lib/libmtdev.so.1"
            fi
            
            export LD_LIBRARY_PATH=${pkgs.libGL}/lib:${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.xorg.libX11}/lib:${pkgs.xorg.libxcb}/lib:${pkgs.mtdev}/lib:$LD_LIBRARY_PATH
            export PYTHONPATH=$PWD/src:$PYTHONPATH
            
            # Configure Poetry to use local virtualenvs
            poetry config virtualenvs.in-project false
            poetry config virtualenvs.path "$POETRY_VENV_PATH"
            poetry config cache-dir "$POETRY_CACHE_DIR"
            
            echo "Development environment setup complete!"
            echo "Poetry cache: $POETRY_CACHE_DIR"
            echo "Virtual envs: $POETRY_VENV_PATH"
            echo ""
            echo "Try running: poetry install && poetry run poe dev"
            echo "you must add (users.users.<youruser>.extraGroups = [ "dialout" ];) in your configuration.nix, and reboot your system!!!" 
          '';
        };
      }
    );
}