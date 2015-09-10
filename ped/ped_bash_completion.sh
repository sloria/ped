#  Completion for ped:
#
#  ped [module name]
#
_complete_ped()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--editor --info --version"

    # --foo options
    if [[ "${cur::1}" == "-" ]]
    then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    case "${prev}" in
    -e|--editor)
        # Complete commands for editor flag
        COMPREPLY=( $(compgen -c ${cur}) )
            return 0
            ;;
    *)
        ;;
    esac

    # Complete a module name
    COMPREPLY=( $(ped --complete ${cur}) )
}
complete -F _complete_ped ped
