{
  description = "Krux-installer flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python314;
        
        libs = with pkgs; [
          libGL
          stdenv.cc.cc.lib
          xorg.libX11
          xorg.libXext
          xorg.libXrender
          xorg.libxcb
          xorg.libXrandr
          xorg.libXinerama
          xorg.libXcursor
          xorg.libXi
          xorg.libXxf86vm
          mtdev
          cairo
          glib
          gtk3
          gdk-pixbuf
          pango
          atk
          freetype
          fontconfig
          zlib
          libffi
        ];
        
        libPath = pkgs.lib.makeLibraryPath libs;
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.uv
            pkgs.git
            pkgs.pkg-config
            pkgs.polkit
            pkgs.openssl
            pkgs.libusb1
            pkgs.tcl
            pkgs.tk
            pkgs.gobject-introspection
          ] ++ libs;
          
          shellHook = ''
            # Project-specific directories
            export PROJECT_ROOT="$(pwd)"
            export PROJECT_DATA="$PROJECT_ROOT/.devenv"
            
            # XDG directories (use existing HOME if set, otherwise use project)
            if [ -z "$HOME" ]; then
              export HOME="$PROJECT_DATA/home"
            fi
            
            export XDG_DATA_HOME="''${XDG_DATA_HOME:-$PROJECT_DATA/share}"
            export XDG_CONFIG_HOME="''${XDG_CONFIG_HOME:-$PROJECT_DATA/config}" 
            export XDG_CACHE_HOME="''${XDG_CACHE_HOME:-$PROJECT_DATA/cache}"
            
            # Create necessary directories
            mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
            
            # Python configuration
            export VIRTUAL_ENV_DISABLE_PROMPT=1
            export UV_CACHE_DIR="$XDG_CACHE_HOME/uv"
            export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"
            mkdir -p "$UV_CACHE_DIR"
            
            # Library paths
            export LD_LIBRARY_PATH="${libPath}:$LD_LIBRARY_PATH"
            
             # Kivy configuration
            export KIVY_NO_CONSOLELOG=1
            

            # Check for dialout group (NixOS specific)
            if command -v nixos-version &> /dev/null; then
              if ! groups | grep -q dialout; then
                echo ""
                echo "⚠️  WARNING: You're not in the 'dialout' group!"
                echo "This is required for USB device access."
                echo ""
                echo "Add this to your configuration.nix:"
                echo "  users.users.<youruser>.extraGroups = ["dialout"];"
                echo ""
                echo "Then rebuild and reboot your system."
                echo ""
              fi
            fi
            
            echo "✓ Development environment ready!"
            echo "  UV cache: $UV_CACHE_DIR"
            echo "  Project data: $PROJECT_DATA"
            echo ""
            echo "Quick start:"
            echo "  uv sync --all-extras && uv run poe dev"
            echo ""
          '';
        };
      }
    );
}