#!/bin/sh
# shellcheck shell=dash
#
# Licensed under the MIT license
# <LICENSE-MIT or https://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

if [ "$KSH_VERSION" = 'Version JM 93t+ 2010-03-05' ]; then
    # The version of ksh93 that ships with many illumos systems does not
    # support the "local" extension.  Print a message rather than fail in
    # subtle ways later on:
    echo 'this installer does not work with this ksh93 version; please try bash!' >&2
    exit 1
fi

set -u

APP_NAME="marzano"
APP_VERSION="0.1.0-alpha.1722910148"
ARTIFACT_DOWNLOAD_URL="${INSTALLER_DOWNLOAD_URL:-https://github.com/getgrit/gritql/releases/download/v0.1.0-alpha.1722910148}"
PRINT_VERBOSE=${INSTALLER_PRINT_VERBOSE:-0}
PRINT_QUIET=${INSTALLER_PRINT_QUIET:-0}
NO_MODIFY_PATH=${INSTALLER_NO_MODIFY_PATH:-0}
read -r RECEIPT <<EORECEIPT
{"binaries":["CARGO_DIST_BINS"],"binary_aliases":{},"install_prefix":"AXO_INSTALL_PREFIX","provider":{"source":"cargo-dist","version":"0.17.0"},"source":{"app_name":"marzano","name":"gritql","owner":"getgrit","release_type":"github"},"version":"0.1.0-alpha.1722910148"}
EORECEIPT
# Are we happy with this same path on Linux and Mac?
RECEIPT_HOME="${HOME}/.config/marzano"

# glibc provided by our Ubuntu 20.04 runners;
# in the future, we should actually record which glibc was on the runner,
# and inject that into the script.
BUILDER_GLIBC_MAJOR="2"
BUILDER_GLIBC_SERIES="31"

usage() {
    # print help (this cat/EOF stuff is a "heredoc" string)
    cat <<EOF
marzano-installer.sh

The installer for marzano 0.1.0-alpha.1722910148

This script detects what platform you're on and fetches an appropriate archive from
https://github.com/getgrit/gritql/releases/download/v0.1.0-alpha.1722910148
then unpacks the binaries and installs them to the first of the following locations

    \$GRIT_INSTALL/bin
    \$HOME/.grit/bin

It will then add that dir to PATH by adding the appropriate line to your shell profiles.

USAGE:
    marzano-installer.sh [OPTIONS]

OPTIONS:
    -v, --verbose
            Enable verbose output

    -q, --quiet
            Disable progress output

        --no-modify-path
            Don't configure the PATH environment variable

    -h, --help
            Print help information
EOF
}

download_binary_and_run_installer() {
    downloader --check
    need_cmd uname
    need_cmd mktemp
    need_cmd chmod
    need_cmd mkdir
    need_cmd rm
    need_cmd tar
    need_cmd grep
    need_cmd cat

    for arg in "$@"; do
        case "$arg" in
            --help)
                usage
                exit 0
                ;;
            --quiet)
                PRINT_QUIET=1
                ;;
            --verbose)
                PRINT_VERBOSE=1
                ;;
            --no-modify-path)
                NO_MODIFY_PATH=1
                ;;
            *)
                OPTIND=1
                if [ "${arg%%--*}" = "" ]; then
                    err "unknown option $arg"
                fi
                while getopts :hvq sub_arg "$arg"; do
                    case "$sub_arg" in
                        h)
                            usage
                            exit 0
                            ;;
                        v)
                            # user wants to skip the prompt --
                            # we don't need /dev/tty
                            PRINT_VERBOSE=1
                            ;;
                        q)
                            # user wants to skip the prompt --
                            # we don't need /dev/tty
                            PRINT_QUIET=1
                            ;;
                        *)
                            err "unknown option -$OPTARG"
                            ;;
                        esac
                done
                ;;
        esac
    done

    get_architecture || return 1
    local _arch="$RETVAL"
    assert_nz "$_arch" "arch"

    local _bins
    local _zip_ext
    local _artifact_name

    # Lookup what to download/unpack based on platform
    case "$_arch" in 
        "aarch64-apple-darwin")
            _artifact_name="marzano-aarch64-apple-darwin.tar.gz"
            _zip_ext=".tar.gz"
            _bins="marzano"
            _bins_js_array='"marzano"'
            _updater_name=""
            _updater_bin=""
            ;;
        "aarch64-unknown-linux-gnu")
            _artifact_name="marzano-aarch64-unknown-linux-gnu.tar.gz"
            _zip_ext=".tar.gz"
            _bins="marzano"
            _bins_js_array='"marzano"'
            _updater_name=""
            _updater_bin=""
            ;;
        "x86_64-apple-darwin")
            _artifact_name="marzano-x86_64-apple-darwin.tar.gz"
            _zip_ext=".tar.gz"
            _bins="marzano"
            _bins_js_array='"marzano"'
            _updater_name=""
            _updater_bin=""
            ;;
        "x86_64-pc-windows-gnu")
            _artifact_name="marzano-x86_64-pc-windows-msvc.tar.gz"
            _zip_ext=".tar.gz"
            _bins="marzano.exe"
            _bins_js_array='"marzano.exe"'
            _updater_name=""
            _updater_bin=""
            ;;
        "x86_64-unknown-linux-gnu")
            _artifact_name="marzano-x86_64-unknown-linux-gnu.tar.gz"
            _zip_ext=".tar.gz"
            _bins="marzano"
            _bins_js_array='"marzano"'
            _updater_name=""
            _updater_bin=""
            ;;
        *)
            err "there isn't a package for $_arch"
            ;;
    esac

    # Replace the placeholder binaries with the calculated array from above
    RECEIPT="$(echo "$RECEIPT" | sed s/'"CARGO_DIST_BINS"'/"$_bins_js_array"/)"

    # download the archive
    local _url="$ARTIFACT_DOWNLOAD_URL/$_artifact_name"
    local _dir
    if ! _dir="$(ensure mktemp -d)"; then
        # Because the previous command ran in a subshell, we must manually
        # propagate exit status.
        exit 1
    fi
    local _file="$_dir/input$_zip_ext"

    say "downloading $APP_NAME $APP_VERSION ${_arch}" 1>&2
    say_verbose "  from $_url" 1>&2
    say_verbose "  to $_file" 1>&2

    ensure mkdir -p "$_dir"

    if ! downloader "$_url" "$_file"; then
      say "failed to download $_url"
      say "this may be a standard network error, but it may also indicate"
      say "that $APP_NAME's release process is not working. When in doubt"
      say "please feel free to open an issue!"
      exit 1
    fi

    # ...and then the updater, if it exists
    if [ -n "$_updater_name" ]; then
        local _updater_url="$ARTIFACT_DOWNLOAD_URL/$_updater_name"
        # This renames the artifact while doing the download, removing the
        # target triple and leaving just the appname-update format
        local _updater_file="$_dir/$APP_NAME-update"

        if ! downloader "$_updater_url" "$_updater_file"; then
          say "failed to download $_updater_url"
          say "this may be a standard network error, but it may also indicate"
          say "that $APP_NAME's release process is not working. When in doubt"
          say "please feel free to open an issue!"
          exit 1
        fi

        # Add the updater to the list of binaries to install
        _bins="$_bins $APP_NAME-update"
    fi

    # unpack the archive
    case "$_zip_ext" in
        ".zip")
            ensure unzip -q "$_file" -d "$_dir"
            ;;

        ".tar."*)
            ensure tar xf "$_file" --strip-components 1 -C "$_dir"
            ;;
        *)
            err "unknown archive format: $_zip_ext"
            ;;
    esac

    install "$_dir" "$_bins" "$_arch" "$@"
    local _retval=$?
    if [ "$_retval" != 0 ]; then
        return "$_retval"
    fi

    ignore rm -rf "$_dir"

    # Install the install receipt
    mkdir -p "$RECEIPT_HOME" || {
        err "unable to create receipt directory at $RECEIPT_HOME"
    }
    echo "$RECEIPT" > "$RECEIPT_HOME/$APP_NAME-receipt.json"
    # shellcheck disable=SC2320
    local _retval=$?

    return "$_retval"
}

# Replaces $HOME with the variable name for display to the user,
# only if $HOME is defined.
replace_home() {
    local _str="$1"

    if [ -n "${HOME:-}" ]; then
        echo "$_str" | sed "s,$HOME,\$HOME,"
    else
        echo "$_str"
    fi
}

json_binary_aliases() {
    local _arch="$1"

    case "$_arch" in 
    "aarch64-apple-darwin")
        echo '{"marzano":["grit"]}'
        ;;
    "aarch64-unknown-linux-gnu")
        echo '{"marzano":["grit"]}'
        ;;
    "x86_64-apple-darwin")
        echo '{"marzano":["grit"]}'
        ;;
    "x86_64-pc-windows-gnu")
        echo '{"marzano.exe":["grit.exe"]}'
        ;;
    "x86_64-unknown-linux-gnu")
        echo '{"marzano":["grit"]}'
        ;;
    esac
}

aliases_for_binary() {
    local _bin="$1"
    local _arch="$2"

    case "$_arch" in 
    "aarch64-apple-darwin")
        case "$_bin" in
            "marzano")
                echo "grit"
            ;;
        *)
            echo ""
            ;;
        esac
        ;;
    "aarch64-unknown-linux-gnu")
        case "$_bin" in
            "marzano")
                echo "grit"
            ;;
        *)
            echo ""
            ;;
        esac
        ;;
    "x86_64-apple-darwin")
        case "$_bin" in
            "marzano")
                echo "grit"
            ;;
        *)
            echo ""
            ;;
        esac
        ;;
    "x86_64-pc-windows-gnu")
        case "$_bin" in
            "marzano.exe")
                echo "grit.exe"
            ;;
        *)
            echo ""
            ;;
        esac
        ;;
    "x86_64-unknown-linux-gnu")
        case "$_bin" in
            "marzano")
                echo "grit"
            ;;
        *)
            echo ""
            ;;
        esac
        ;;
    esac
}

# See discussion of late-bound vs early-bound for why we use single-quotes with env vars
# shellcheck disable=SC2016
install() {
    # This code needs to both compute certain paths for itself to write to, and
    # also write them to shell/rc files so that they can look them up to e.g.
    # add them to PATH. This requires an active distinction between paths
    # and expressions that can compute them.
    #
    # The distinction lies in when we want env-vars to be evaluated. For instance
    # if we determine that we want to install to $HOME/.myapp, which do we add
    # to e.g. $HOME/.profile:
    #
    # * early-bound: export PATH="/home/myuser/.myapp:$PATH"
    # * late-bound:  export PATH="$HOME/.myapp:$PATH"
    #
    # In this case most people would prefer the late-bound version, but in other
    # cases the early-bound version might be a better idea. In particular when using
    # other env-vars than $HOME, they are more likely to be only set temporarily
    # for the duration of this install script, so it's more advisable to erase their
    # existence with early-bounding.
    #
    # This distinction is handled by "double-quotes" (early) vs 'single-quotes' (late).
    #
    # However if we detect that "$SOME_VAR/..." is a subdir of $HOME, we try to rewrite
    # it to be '$HOME/...' to get the best of both worlds.
    #
    # This script has a few different variants, the most complex one being the
    # CARGO_HOME version which attempts to install things to Cargo's bin dir,
    # potentially setting up a minimal version if the user hasn't ever installed Cargo.
    #
    # In this case we need to:
    #
    # * Install to $HOME/.cargo/bin/
    # * Create a shell script at $HOME/.cargo/env that:
    #   * Checks if $HOME/.cargo/bin/ is on PATH
    #   * and if not prepends it to PATH
    # * Edits $HOME/.profile to run $HOME/.cargo/env (if the line doesn't exist)
    #
    # To do this we need these 4 values:

    # The actual path we're going to install to
    local _install_dir
    # The install prefix we write to the receipt.
    # For organized install methods like CargoHome, which have
    # subdirectories, this is the root without `/bin`. For other
    # methods, this is the same as `_install_dir`.
    local _receipt_install_dir
    # Path to the an shell script that adds install_dir to PATH
    local _env_script_path
    # Potentially-late-bound version of install_dir to write env_script
    local _install_dir_expr
    # Potentially-late-bound version of env_script_path to write to rcfiles like $HOME/.profile
    local _env_script_path_expr

    # Before actually consulting the configured install strategy, see
    # if we're overriding it.
    if [ -n "${CARGO_DIST_FORCE_INSTALL_DIR:-}" ]; then
        _install_dir="$CARGO_DIST_FORCE_INSTALL_DIR"
        _receipt_install_dir="$_install_dir"
        _env_script_path="$CARGO_DIST_FORCE_INSTALL_DIR/env"
        _install_dir_expr="$(replace_home "$CARGO_DIST_FORCE_INSTALL_DIR")"
        _env_script_path_expr="$(replace_home "$CARGO_DIST_FORCE_INSTALL_DIR/env")"
    fi
    if [ -z "${_install_dir:-}" ]; then
        # Install to $GRIT_INSTALL/bin
        if [ -n "${GRIT_INSTALL:-}" ]; then
            _install_dir="$GRIT_INSTALL/bin"
            _receipt_install_dir="$_install_dir"
            _env_script_path="$GRIT_INSTALL/bin/env"
            _install_dir_expr="$(replace_home "$_install_dir")"
            _env_script_path_expr="$(replace_home "$_env_script_path")"
        fi
    fi
    if [ -z "${_install_dir:-}" ]; then
        # Install to $HOME/.grit/bin
        if [ -n "${HOME:-}" ]; then
            _install_dir="$HOME/.grit/bin"
            _receipt_install_dir="$_install_dir"
            _env_script_path="$HOME/.grit/bin/env"
            _install_dir_expr='$HOME/.grit/bin'
            _env_script_path_expr='$HOME/.grit/bin/env'
        fi
    fi

    if [ -z "$_install_dir_expr" ]; then
        err "could not find a valid path to install to!"
    fi

    # Identical to the sh version, just with a .fish file extension
    # We place it down here to wait until it's been assigned in every
    # path.
    _fish_env_script_path="${_env_script_path}.fish"
    _fish_env_script_path_expr="${_env_script_path_expr}.fish"

    # Replace the temporary cargo home with the calculated one
    RECEIPT=$(echo "$RECEIPT" | sed "s,AXO_INSTALL_PREFIX,$_receipt_install_dir,")
    # Also replace the aliases with the arch-specific one
    RECEIPT=$(echo "$RECEIPT" | sed "s'\"binary_aliases\":{}'\"binary_aliases\":$(json_binary_aliases "$_arch")'")

    say "installing to $_install_dir"
    ensure mkdir -p "$_install_dir"

    # copy all the binaries to the install dir
    local _src_dir="$1"
    local _bins="$2"
    local _arch="$3"
    for _bin_name in $_bins; do
        local _bin="$_src_dir/$_bin_name"
        ensure mv "$_bin" "$_install_dir"
        # unzip seems to need this chmod
        ensure chmod +x "$_install_dir/$_bin_name"
        for _dest in $(aliases_for_binary "$_bin_name" "$_arch"); do
            ln -sf "$_install_dir/$_bin_name" "$_install_dir/$_dest"
        done
        say "  $_bin_name"
    done

    say "everything's installed!"

    if [ "0" = "$NO_MODIFY_PATH" ]; then
        add_install_dir_to_ci_path "$_install_dir"
        add_install_dir_to_path "$_install_dir_expr" "$_env_script_path" "$_env_script_path_expr" ".profile" "sh"
        exit1=$?
        add_install_dir_to_path "$_install_dir_expr" "$_env_script_path" "$_env_script_path_expr" ".bash_profile .bash_login .bashrc" "sh"
        exit2=$?
        add_install_dir_to_path "$_install_dir_expr" "$_env_script_path" "$_env_script_path_expr" ".zshrc .zshenv" "sh"
        exit3=$?
        # This path may not exist by default
        ensure mkdir -p "$HOME/.config/fish/conf.d"
        exit4=$?
        add_install_dir_to_path "$_install_dir_expr" "$_fish_env_script_path" "$_fish_env_script_path_expr" ".config/fish/conf.d/$APP_NAME.env.fish" "fish"
        exit5=$?

        if [ "${exit1:-0}" = 1 ] || [ "${exit2:-0}" = 1 ] || [ "${exit3:-0}" = 1 ] || [ "${exit4:-0}" = 1 ] || [ "${exit5:-0}" = 1 ]; then
            say ""
            say "To add $_install_dir_expr to your PATH, either restart your shell or run:"
            say ""
            say "    source $_env_script_path_expr (sh, bash, zsh)"
            say "    source $_fish_env_script_path_expr (fish)"
        fi
    fi
}

print_home_for_script() {
    local script="$1"

    local _home
    case "$script" in
        # zsh has a special ZDOTDIR directory, which if set
        # should be considered instead of $HOME
        .zsh*)
            if [ -n "${ZDOTDIR:-}" ]; then
                _home="$ZDOTDIR"
            else
                _home="$HOME"
            fi
            ;;
        *)
            _home="$HOME"
            ;;
    esac

    echo "$_home"
}

add_install_dir_to_ci_path() {
    # Attempt to do CI-specific rituals to get the install-dir on PATH faster
    local _install_dir="$1"

    # If GITHUB_PATH is present, then write install_dir to the file it refs.
    # After each GitHub Action, the contents will be added to PATH.
    # So if you put a curl | sh for this script in its own "run" step,
    # the next step will have this dir on PATH.
    #
    # Note that GITHUB_PATH will not resolve any variables, so we in fact
    # want to write install_dir and not install_dir_expr
    if [ -n "${GITHUB_PATH:-}" ]; then
        ensure echo "$_install_dir" >> "$GITHUB_PATH"
    fi
}

add_install_dir_to_path() {
    # Edit rcfiles ($HOME/.profile) to add install_dir to $PATH
    #
    # We do this slightly indirectly by creating an "env" shell script which checks if install_dir
    # is on $PATH already, and prepends it if not. The actual line we then add to rcfiles
    # is to just source that script. This allows us to blast it into lots of different rcfiles and
    # have it run multiple times without causing problems. It's also specifically compatible
    # with the system rustup uses, so that we don't conflict with it.
    local _install_dir_expr="$1"
    local _env_script_path="$2"
    local _env_script_path_expr="$3"
    local _rcfiles="$4"
    local _shell="$5"

    if [ -n "${HOME:-}" ]; then
        local _target
        local _home

        # Find the first file in the array that exists and choose
        # that as our target to write to
        for _rcfile_relative in $_rcfiles; do
            _home="$(print_home_for_script "$_rcfile_relative")"
            local _rcfile="$_home/$_rcfile_relative"

            if [ -f "$_rcfile" ]; then
                _target="$_rcfile"
                break
            fi
        done

        # If we didn't find anything, pick the first entry in the
        # list as the default to create and write to
        if [ -z "${_target:-}" ]; then
            local _rcfile_relative
            _rcfile_relative="$(echo "$_rcfiles" | awk '{ print $1 }')"
            _home="$(print_home_for_script "$_rcfile_relative")"
            _target="$_home/$_rcfile_relative"
        fi

        # `source x` is an alias for `. x`, and the latter is more portable/actually-posix.
        # This apparently comes up a lot on freebsd. It's easy enough to always add
        # the more robust line to rcfiles, but when telling the user to apply the change
        # to their current shell ". x" is pretty easy to misread/miscopy, so we use the
        # prettier "source x" line there. Hopefully people with Weird Shells are aware
        # this is a thing and know to tweak it (or just restart their shell).
        local _robust_line=". \"$_env_script_path_expr\""
        local _pretty_line="source \"$_env_script_path_expr\""

        # Add the env script if it doesn't already exist
        if [ ! -f "$_env_script_path" ]; then
            say_verbose "creating $_env_script_path"
            if [ "$_shell" = "sh" ]; then
                write_env_script_sh "$_install_dir_expr" "$_env_script_path"
            else
                write_env_script_fish "$_install_dir_expr" "$_env_script_path"
            fi
        else
            say_verbose "$_env_script_path already exists"
        fi

        # Check if the line is already in the rcfile
        # grep: 0 if matched, 1 if no match, and 2 if an error occurred
        #
        # Ideally we could use quiet grep (-q), but that makes "match" and "error"
        # have the same behaviour, when we want "no match" and "error" to be the same
        # (on error we want to create the file, which >> conveniently does)
        #
        # We search for both kinds of line here just to do the right thing in more cases.
        if ! grep -F "$_robust_line" "$_target" > /dev/null 2>/dev/null && \
           ! grep -F "$_pretty_line" "$_target" > /dev/null 2>/dev/null
        then
            # If the script now exists, add the line to source it to the rcfile
            # (This will also create the rcfile if it doesn't exist)
            if [ -f "$_env_script_path" ]; then
                local _line
                # Fish has deprecated `.` as an alias for `source` and
                # it will be removed in a later version.
                # https://fishshell.com/docs/current/cmds/source.html
                # By contrast, `.` is the traditional syntax in sh and
                # `source` isn't always supported in all circumstances.
                if [ "$_shell" = "fish" ]; then
                    _line="$_pretty_line"
                else
                    _line="$_robust_line"
                fi
                say_verbose "adding $_line to $_target"
                # prepend an extra newline in case the user's file is missing a trailing one
                ensure echo "" >> "$_target"
                ensure echo "$_line" >> "$_target"
                return 1
            fi
        else
            say_verbose "$_install_dir already on PATH"
        fi
    fi
}

write_env_script_sh() {
    # write this env script to the given path (this cat/EOF stuff is a "heredoc" string)
    local _install_dir_expr="$1"
    local _env_script_path="$2"
    ensure cat <<EOF > "$_env_script_path"
#!/bin/sh
# add binaries to PATH if they aren't added yet
# affix colons on either side of \$PATH to simplify matching
case ":\${PATH}:" in
    *:"$_install_dir_expr":*)
        ;;
    *)
        # Prepending path in case a system-installed binary needs to be overridden
        export PATH="$_install_dir_expr:\$PATH"
        ;;
esac
EOF
}

write_env_script_fish() {
    # write this env script to the given path (this cat/EOF stuff is a "heredoc" string)
    local _install_dir_expr="$1"
    local _env_script_path="$2"
    ensure cat <<EOF > "$_env_script_path"
if not contains "$_install_dir_expr" \$PATH
    # Prepending path in case a system-installed binary needs to be overridden
    set -x PATH "$_install_dir_expr" \$PATH
end
EOF
}

check_proc() {
    # Check for /proc by looking for the /proc/self/exe link
    # This is only run on Linux
    if ! test -L /proc/self/exe ; then
        err "fatal: Unable to find /proc/self/exe.  Is /proc mounted?  Installation cannot proceed without /proc."
    fi
}

get_bitness() {
    need_cmd head
    # Architecture detection without dependencies beyond coreutils.
    # ELF files start out "\x7fELF", and the following byte is
    #   0x01 for 32-bit and
    #   0x02 for 64-bit.
    # The printf builtin on some shells like dash only supports octal
    # escape sequences, so we use those.
    local _current_exe_head
    _current_exe_head=$(head -c 5 /proc/self/exe )
    if [ "$_current_exe_head" = "$(printf '\177ELF\001')" ]; then
        echo 32
    elif [ "$_current_exe_head" = "$(printf '\177ELF\002')" ]; then
        echo 64
    else
        err "unknown platform bitness"
    fi
}

is_host_amd64_elf() {
    need_cmd head
    need_cmd tail
    # ELF e_machine detection without dependencies beyond coreutils.
    # Two-byte field at offset 0x12 indicates the CPU,
    # but we're interested in it being 0x3E to indicate amd64, or not that.
    local _current_exe_machine
    _current_exe_machine=$(head -c 19 /proc/self/exe | tail -c 1)
    [ "$_current_exe_machine" = "$(printf '\076')" ]
}

get_endianness() {
    local cputype=$1
    local suffix_eb=$2
    local suffix_el=$3

    # detect endianness without od/hexdump, like get_bitness() does.
    need_cmd head
    need_cmd tail

    local _current_exe_endianness
    _current_exe_endianness="$(head -c 6 /proc/self/exe | tail -c 1)"
    if [ "$_current_exe_endianness" = "$(printf '\001')" ]; then
        echo "${cputype}${suffix_el}"
    elif [ "$_current_exe_endianness" = "$(printf '\002')" ]; then
        echo "${cputype}${suffix_eb}"
    else
        err "unknown platform endianness"
    fi
}

get_architecture() {
    local _ostype
    local _cputype
    _ostype="$(uname -s)"
    _cputype="$(uname -m)"
    local _clibtype="gnu"
    local _local_glibc

    if [ "$_ostype" = Linux ]; then
        if [ "$(uname -o)" = Android ]; then
            _ostype=Android
        fi
        if ldd --version 2>&1 | grep -q 'musl'; then
            _clibtype="musl-dynamic"
        # glibc, but is it a compatible glibc?
        else
            # Parsing version out from line 1 like:
            # ldd (Ubuntu GLIBC 2.35-0ubuntu3.1) 2.35
            _local_glibc="$(ldd --version | awk -F' ' '{ if (FNR<=1) print $NF }')"

            if [ "$(echo "${_local_glibc}" | awk -F. '{ print $1 }')" = $BUILDER_GLIBC_MAJOR ] && [ "$(echo "${_local_glibc}" | awk -F. '{ print $2 }')" -ge $BUILDER_GLIBC_SERIES ]; then
                _clibtype="gnu"
            else
                say "System glibc version (\`${_local_glibc}') is too old; using musl" >&2
                _clibtype="musl-static"
            fi
        fi
    fi

    if [ "$_ostype" = Darwin ] && [ "$_cputype" = i386 ]; then
        # Darwin `uname -m` lies
        if sysctl hw.optional.x86_64 | grep -q ': 1'; then
            _cputype=x86_64
        fi
    fi

    if [ "$_ostype" = Darwin ] && [ "$_cputype" = x86_64 ]; then
        # Rosetta on aarch64
        if [ "$(sysctl -n hw.optional.arm64 2>/dev/null)" = "1" ]; then
            _cputype=aarch64
        fi
    fi

    if [ "$_ostype" = SunOS ]; then
        # Both Solaris and illumos presently announce as "SunOS" in "uname -s"
        # so use "uname -o" to disambiguate.  We use the full path to the
        # system uname in case the user has coreutils uname first in PATH,
        # which has historically sometimes printed the wrong value here.
        if [ "$(/usr/bin/uname -o)" = illumos ]; then
            _ostype=illumos
        fi

        # illumos systems have multi-arch userlands, and "uname -m" reports the
        # machine hardware name; e.g., "i86pc" on both 32- and 64-bit x86
        # systems.  Check for the native (widest) instruction set on the
        # running kernel:
        if [ "$_cputype" = i86pc ]; then
            _cputype="$(isainfo -n)"
        fi
    fi

    case "$_ostype" in

        Android)
            _ostype=linux-android
            ;;

        Linux)
            check_proc
            _ostype=unknown-linux-$_clibtype
            _bitness=$(get_bitness)
            ;;

        FreeBSD)
            _ostype=unknown-freebsd
            ;;

        NetBSD)
            _ostype=unknown-netbsd
            ;;

        DragonFly)
            _ostype=unknown-dragonfly
            ;;

        Darwin)
            _ostype=apple-darwin
            ;;

        illumos)
            _ostype=unknown-illumos
            ;;

        MINGW* | MSYS* | CYGWIN* | Windows_NT)
            _ostype=pc-windows-gnu
            ;;

        *)
            err "unrecognized OS type: $_ostype"
            ;;

    esac

    case "$_cputype" in

        i386 | i486 | i686 | i786 | x86)
            _cputype=i686
            ;;

        xscale | arm)
            _cputype=arm
            if [ "$_ostype" = "linux-android" ]; then
                _ostype=linux-androideabi
            fi
            ;;

        armv6l)
            _cputype=arm
            if [ "$_ostype" = "linux-android" ]; then
                _ostype=linux-androideabi
            else
                _ostype="${_ostype}eabihf"
            fi
            ;;

        armv7l | armv8l)
            _cputype=armv7
            if [ "$_ostype" = "linux-android" ]; then
                _ostype=linux-androideabi
            else
                _ostype="${_ostype}eabihf"
            fi
            ;;

        aarch64 | arm64)
            _cputype=aarch64
            ;;

        x86_64 | x86-64 | x64 | amd64)
            _cputype=x86_64
            ;;

        mips)
            _cputype=$(get_endianness mips '' el)
            ;;

        mips64)
            if [ "$_bitness" -eq 64 ]; then
                # only n64 ABI is supported for now
                _ostype="${_ostype}abi64"
                _cputype=$(get_endianness mips64 '' el)
            fi
            ;;

        ppc)
            _cputype=powerpc
            ;;

        ppc64)
            _cputype=powerpc64
            ;;

        ppc64le)
            _cputype=powerpc64le
            ;;

        s390x)
            _cputype=s390x
            ;;
        riscv64)
            _cputype=riscv64gc
            ;;
        loongarch64)
            _cputype=loongarch64
            ;;
        *)
            err "unknown CPU type: $_cputype"

    esac

    # Detect 64-bit linux with 32-bit userland
    if [ "${_ostype}" = unknown-linux-gnu ] && [ "${_bitness}" -eq 32 ]; then
        case $_cputype in
            x86_64)
                # 32-bit executable for amd64 = x32
                if is_host_amd64_elf; then {
                    err "x32 linux unsupported"
                }; else
                    _cputype=i686
                fi
                ;;
            mips64)
                _cputype=$(get_endianness mips '' el)
                ;;
            powerpc64)
                _cputype=powerpc
                ;;
            aarch64)
                _cputype=armv7
                if [ "$_ostype" = "linux-android" ]; then
                    _ostype=linux-androideabi
                else
                    _ostype="${_ostype}eabihf"
                fi
                ;;
            riscv64gc)
                err "riscv64 with 32-bit userland unsupported"
                ;;
        esac
    fi

    # treat armv7 systems without neon as plain arm
    if [ "$_ostype" = "unknown-linux-gnueabihf" ] && [ "$_cputype" = armv7 ]; then
        if ensure grep '^Features' /proc/cpuinfo | grep -q -v neon; then
            # At least one processor does not have NEON.
            _cputype=arm
        fi
    fi

    _arch="${_cputype}-${_ostype}"

    RETVAL="$_arch"
}

say() {
    if [ "0" = "$PRINT_QUIET" ]; then
        echo "$1"
    fi
}

say_verbose() {
    if [ "1" = "$PRINT_VERBOSE" ]; then
        echo "$1"
    fi
}

err() {
    if [ "0" = "$PRINT_QUIET" ]; then
        local red
        local reset
        red=$(tput setaf 1 2>/dev/null || echo '')
        reset=$(tput sgr0 2>/dev/null || echo '')
        say "${red}ERROR${reset}: $1" >&2
    fi
    exit 1
}

need_cmd() {
    if ! check_cmd "$1"
    then err "need '$1' (command not found)"
    fi
}

check_cmd() {
    command -v "$1" > /dev/null 2>&1
    return $?
}

assert_nz() {
    if [ -z "$1" ]; then err "assert_nz $2"; fi
}

# Run a command that should never fail. If the command fails execution
# will immediately terminate with an error showing the failing
# command.
ensure() {
    if ! "$@"; then err "command failed: $*"; fi
}

# This is just for indicating that commands' results are being
# intentionally ignored. Usually, because it's being executed
# as part of error handling.
ignore() {
    "$@"
}

# This wraps curl or wget. Try curl first, if not installed,
# use wget instead.
downloader() {
    if check_cmd curl
    then _dld=curl
    elif check_cmd wget
    then _dld=wget
    else _dld='curl or wget' # to be used in error message of need_cmd
    fi

    if [ "$1" = --check ]
    then need_cmd "$_dld"
    elif [ "$_dld" = curl ]
    then curl -sSfL "$1" -o "$2"
    elif [ "$_dld" = wget ]
    then wget "$1" -O "$2"
    else err "Unknown downloader"   # should not reach here
    fi
}

download_binary_and_run_installer "$@" || exit 1
