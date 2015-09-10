#compdef ped
# vim: ft=zsh sw=2 ts=2 et
# ZSH completion file for ped.

_ped() {
    local curcontext="$curcontext" state line
    integer NORMARG
    typeset -A opt_args

    _arguments -C -s -n \
      '(- -h --help)'{-h,--help}'[Show help message]' \
      '(- -v --version)'{-v,--version}'[Print version and exit]' \
      '(- -e --editor)'{-e,--editor}'[Editor to use]' \
      '(- -i --info)'{-i,--info}'[Print module name, path, and line number]' \
      '1: :->module'

    case $state in
    module)
      if [[ CURRENT -eq NORMARG ]]
      then
        # If the current argument is the first non-option argument
        # then complete with python modules
        cmds=( ${(uf)"$(ped ${words[CURRENT]} --complete)"} )
        _arguments '1:modules:(${cmds})'
        _message -e patterns 'pattern' && ret=0
      fi
    ;;
    *)
    esac
}

_ped "$@"
