# vim: expandtab foldmethod=marker :
"""A not so generic CLI library"""

"""
TODO:   config file support
        the actual nodes in the CLI tree should mostly come from a 
        configuration of some sort. There would of course be built-ins like
        'exit', 'configure' and so forth, but for example 'ping' in 
        operational mode or all the configuration mode nodes should be read at
        startup and merged with the built-ins

TODO:   set the standard for branch / leaf / leaf-bool and so forth
TODO:   introduce hidden nodes
"""


class Cli:
    use_rawinput = 1
    stop = None

    mode = 'operational'

    ct_oper = []
    ct_oper.append("quit")
    ct_oper.append("configure")
    ct_oper.append("ping")

    ct_config = []
    ct_config.append("abort")
    ct_config.append("annotate")
    ct_config.append("edit")
    ct_config.append("quit")
    ct_config.append("set")
    ct_config.append("status")

    tree_config = [
            {   # abort (abort the current transaction
                'tree_type' : 'branch',
                'name'      : 'abort',
                'shorthelp' : 'Abort the current transaction'
            },
            {   # delete
                'tree_type' : 'branch',
                'name'      : 'delete',
                'kids'      : [ ]
            },
            {   # edit
                'tree_type' : 'branch',
                'name'      : 'edit'
            },
            {   # exit
                'tree_type' : 'branch',
                'name'      : 'exit',
                'command'   : 'self.exit()',
                'hidden'    : True
            },
            {   # quit
                'tree_type' : 'branch',
                'name'      : 'quit',
                'command'   : 'self.exit()'
            },
            {   # set
                'tree_type' : 'branch',
                'name'      : 'set'
            }
        ]

    tree_configuration = [
                {   # firewall
                    'tree_type' : 'branch',
                    'name'      : 'firewall'
                },
                {   # interfaces
                    'tree_type': 'branch',
                    'name': 'interfaces',
                    'shorthelp': 'Interface configuration'
                },
                {   # protocols
                    'tree_type' : 'branch',
                    'name': 'protocols'
                },
                {   # system
                    'tree_type' : 'branch',
                    'name': 'system'
                }
            ]

    tree_operational =   [
                {   # configure
                    'tree_type' : 'branch',
                    'name'      : 'configure',
                    'command'   : 'self.mode_configure()',
                    'shorthelp' : 'Enter configuration mode'
                },
                {   # exit
                    'tree_type' : 'branch',
                    'name'      : 'exit',
                    'command'   : 'self.exit()',
                    'hidden'    : True,
                    'shorthelp' : ''
                },
                {   # logout
                    'tree_type' : 'branch',
                    'name'      : 'logout',
                    'command'   : 'self.exit()',
                    'hidden'    : True,
                    'shorthelp' : ''
                },
                {   # ping
                    'tree_type' : 'branch',
                    'name'      : 'ping',
                    'command'   : 'self.ping(tokens)',
                    'shorthelp' : 'ping a host',
                    'kids': [
                                {   # host
                                    'tree_type' : 'value',
                                    'name'      : '<host>',
                                    'value_type': [ 'host', 'ip', 'ip6' ],
                                    'shorthelp' : 'Hostname or IP(v6) address of remote host'
                                },
                                {   # do-not-fragment
                                    'tree_type' : 'leaf-bool',
                                    'name'      : 'do-not-fragment',
                                    'shorthelp' : 'Do not fragment the ICMP echo request packets'
                                },
                                {   # size
                                    'tree_type' : 'leaf',
                                    'name'      : 'size',
                                    'shorthelp' : 'Size of ICMP echo request in bytes (+8 bytes of header)'
                                },
                                {   # ttl
                                    'tree_type' : 'leaf',
                                    'name'      : 'ttl',
                                    'value_type': [ 'ttl' ],
                                    'shorthelp' : 'TTL (hop-limit for IPv6)'
                                }
                            ]
                },
                {   # show
                    'tree_type' : 'branch',
                    'name'      : 'show',
                    'shorthelp' : 'Show information'
                },
                {   # traceroute
                    'tree_type' : 'branch',
                    'name'      : 'traceroute',
                    'shorthelp' : 'trace the path to a host'
                },
                {   # quit
                    'tree_type' : 'branch',
                    'name'      : 'quit',
                    'command'   : 'self.exit()',
                    'shorthelp' : 'Log out from the CLI / router'
                }
            ]



    try:
        from copy import copy
    except ImportError:
        print "Unable to import 'copy' library, exiting..."
        sys.exit(1)

    def __init__(self):
        import sys
        self.stdin = sys.stdin
        self.stdout = sys.stdout

        self.prompt_update()

    def exit(self): # {{{
        import sys
        if self.mode == 'operational':
            sys.exit(0);
        else:
            self.mode_operational()
    # }}}

    def prompt_update(self): # {{{
        import os
        username = os.environ.get('USER')
        if username == None:
            username = 'user'
        hostname = os.uname()[1]
        self.prompt = username + "@" + hostname
        if self.mode == 'operational':
            self.prompt = self.prompt + "> "
        else:
            self.prompt = self.prompt + "# "
    # }}}

    def mode_configure(self): # {{{
        if self.mode == 'operational':
            print "Entering configuration mode"
            self.mode = 'configure'
            self.prompt_update()
# }}}

    def mode_operational(self): #{{{
        if self.mode == 'configure':
            print "Exiting configuration mode"
            self.mode = 'operational'
            self.prompt_update()
# }}}

    def pre_input_hook(self): # {{{
        pass
    # }}}

    def rprint(self, text): # {{{
        if text[-1] != '\n':
            text = text + " "
        self.stdout.write(text)
        self.stdout.flush()
    # }}}
    
    def loop(self): #{{{
        if self.use_rawinput:
            try:
                import readline
                self.old_completer = readline.get_completer()
                """
                We want to list help stuff on ? but we can't really:
                    http://bugs.python.org/issue1690201
                Pretty much the same thing with space, where we want
                tab completion, though not tab help display
                """
                readline.set_completer(self.tab_complete)
                readline.parse_and_bind('tab: complete')
                readline.parse_and_bind('?: "\C-v?\t\t\C-h"')
#                readline.parse_and_bind('space: complete')
#                readline.parse_and_bind('?: list_completions')
            except ImportError:
                pass
        try:
            while not self.stop:
                readline.set_pre_input_hook(self.pre_input_hook)
                if self.use_rawinput:
                    try:
                        line = raw_input(self.prompt)
                    except EOFError:
                        line = 'EOF'
                else:
                    self.rprint(self.prompt)
                    line = self.stdin.readline()
                    if not len(line):
                        line = 'EOF'
                    else:
                        line = line[:-1] # chop \n
                line = self.precmd(line)
                self.stop = self.evalcmd(line)
#                stop = self.postcmd(stop, line)
  #          self.postloop()
        finally:
            if self.use_rawinput:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass
# }}}

    def evalcmd(self, opt_line): # {{{
        from copy import copy
        import re
        line = re.sub(' $', '', opt_line)
        tokens = line.split()
        all_tokens = copy(tokens)

        if self.mode == 'operational':
            data = self.traverse(self.tree_operational, 1, tokens, all_tokens)
        else:
            data = self.traverse(self.tree_config, 1, tokens, all_tokens)

        try:
            command = data['command']
        except:
            print "No command available!"
        else:
            eval(data['command'])
    # }}}

    def precmd(self, line): # {{{
        """
        precmd is for doing any funky stuff before the line is parsed
        """
        return line
    # }}}

    def postcmd(self, line): # {{{
        """
        postcmd is for doing any funky stuff after each parsed line
        """
        return None
    # }}}

    def tab_print(self, matches, num_matches, max_length): # {{{
        print "in tab_print"
        import readline
        import re
        txt = readline.get_line_buffer()
        self.rprint("\n")
        for i in num_matches:
            if re.match('<', i):
                continue
            line = "%s   " % i
            self.rprint(line)
        self.rprint("\n")
        if len(txt) > 0:
            self.rprint(self.prompt[0:-1] + " " + txt[0:-1])
        else:
            self.rprint(self.prompt[0:-1])
    # }}}

    def shorthelp_print(self, matches, num_matches, max_length): # {{{
        import readline
        from copy import copy
        raw_txt = readline.get_line_buffer()
        txt = raw_txt[0:-1]
        tokens = txt.split()

        try:
            last_token = tokens[-1]
        except:
            last_token = ""
        if txt[-1:] == ' ':
            last_token = ""

        if len(tokens) > 0 and txt[-1:] != ' ':
            tokens.pop()
        all_tokens = copy(tokens)

        if self.mode == 'operational':
            data = self.traverse(self.tree_operational, 1, tokens, all_tokens)
        else:
            data = self.traverse(self.tree_config, 1, tokens, all_tokens)

        self.rprint("\nPossible completions:\n")
        for ii in num_matches:
            if ii[-1] == ' ':
                i = ii.rsplit()[0]
            else:
                i = ii

            for obj in data:
                if obj['name'][0:len(last_token)] != last_token:
                    continue
                if obj['name'] == i:
                    try:
                        line = "  %-15s %s\n" % (i, obj['shorthelp'])
                    except:
                        line = "  %-15s\n" % (i)
                    self.rprint(line)
        self.rprint(self.prompt + txt)
    # }}}

    def traverse(self, data, level, tokens, all_tokens): # {{{
        """
        data is the config tree given to us
        level is how far down we've dived into the tree
        tokens contains the current line entered by the user in tokenized form
            the first value is popped for each time traverse is called 
            (recursively)
        all_tokens is the same as tokens though it is never reduced
        """
        # if tokens == 0 then we are as deep as we can dive into the structure
        # and so we just return data
        if len(tokens) == 0:
            return data

        # 
#        ct = tokens.pop(0)
        ct = tokens[0]
        for obj in data:
            if obj['tree_type'] == 'branch' and obj['name'] == ct:
                tokens.pop(0)
                try:
                    return self.traverse(obj['kids'], level+1, tokens, all_tokens)
                except:
                    return obj

        # fallback!
        return data
    # }}}

    def tab_complete(self, text, state): # {{{
        """Return the next possible completion for 'text'.

        This is called successively with state == 0, 1, 2, ... until it
        returns None.  The completion should begin with 'text'.

        """

        # TODO: we should probably do some syntax and value validation here as well

        """
        -- Flow --
        complete or display shorthelp?

        1) Tokenize input
        2) Where are we right now in the CLI structure?
        3) Do a lookup on how the list of possible completions should be 
           sought
        4) Get the list of all completions on this level
        5) Match it up with whatever the user might already have written
        """
        from copy import copy
        import readline
        txt = readline.get_line_buffer()

        tokens = txt.split()
        if len(tokens) > 0 and txt[-1:] != ' ':
            tokens.pop()
        all_tokens = copy(tokens)

        """ TODO: fix this ? shit! """
        if (txt[-1:] == '?'):
            readline.set_completion_display_matches_hook(self.shorthelp_print)
        else:
            readline.set_completion_display_matches_hook(self.tab_print)

        if self.mode == 'operational':
            data = self.traverse(self.tree_operational, 1, tokens, all_tokens)
        else:
            data = self.traverse(self.tree_config, 1, tokens, all_tokens)


        # if last token is a leaf, then it requires a value and so we simply
        # return an empty list since we don't do value completion yet
        if len(tokens) > 0:
            lc = tokens[-1:][0]
            for obj in data:
                if obj['name'] == lc:
                    if obj['tree_type'] == 'leaf':
                        return []

        # fallback?
        if len(tokens) > 0:
            result = []
            for obj in data:
#                if obj['tree_type'] == 'value':
#                    continue
                if obj['name'] not in all_tokens:
                    result.append(obj)
            data = copy(result)


        # don't append 'value' types to tab-completion
        # ie, 'ping ttl <value>' should not have '<value>' be completed
        ac = []
        for obj in data:
            if obj['tree_type'] != 'value':
                pass
            try:
                if obj['hidden'] == True:
                    continue
            except:
                ac.append(obj['name'])

        pc = []

        """ 4) Match it up with whatever the user might already have written
        """
        for val in ac:
            if val[0:len(text)] == text:
                pc.append(val)
#            if val.find(text) != -1:
#                pc.append(val + " ")

        try:
            return pc[state]
        except:
            return None
    # }}}

