import ply.yacc as yacc
from .lexer import  MonLexer
from src.io.event_handlers.switch_team import SwitchTeamEventHandler

class BadMessageException(Exception):
  pass

class MonParser(object):
    def parse(self, payload):
        res = self._parser.parse(payload)
        #print(res)
        if res:
          return res
        else:
          raise BadMessageException

    def test(self, data):
        res = self._parser.parse(data)
        print(res)

    def __init__(self, the_lexer=None):
        if the_lexer is None:
            the_lexer = MonLexer()
        self._lexer = the_lexer
        the_lexer.build()
        self.tokens = self._lexer.tokens

        self._parser = yacc.yacc(module=self)


#    def p_term_player_enter_leave(self,p):
#            '''expression : pterm ENTERED
#                            | pterm DISCONNECTED REASON'''
#            p[0] = p[1]

    def p_expression_entered_game(self, p):
            'expression : pterm ENTERED'
            p[0] = "{}".format(p[1])
            #self.out = 

    def p_expression_switch(self,p):
            'expression : pterm SWITCH TEAM TO TEAM'
            p[0] = "{} {} {}".format(p[1], p[3], p[5])
            #p[0] = p[1] 
            #self.out = SwitchTeamEventHandler(


    def p_expression_assist(self,p):
            'expression : pterm ASSIST pterm'
            p[0]= "{} {} {}".format(p[1], p[2], p[3])

    def p_expression_defuse(self,p):
            'expression : pterm TRIGGERED DEFUSEBOMB'
            p[0]= "{} {}".format(p[1], p[3])

    def p_expression_plant(self,p):
            'expression : pterm TRIGGERED PLANTBOMB'
            p[0]= "{} {}".format(p[1], p[3])

    def p_expression_attack(self,p):
            'expression : pterm POS ATTACKED pterm POS WITH WEAPON ATTACK ATTACK ATTACK ATTACK HITGROUP'
            p[0]= "{} {} {} {} {} {} {}".format(p[1], p[2], p[3], p[4], p[5], p[7], p[12])

    def p_expression_kill(self,p):
            '''expression : pterm POS KILLED pterm POS WITH WEAPON 
                            | pterm POS KILLED pterm POS WITH WEAPON HEADSHOT'''
            if len(p)==8 :
                p[0] = "{} {} {} {} {} {}".format(p[1], p[2], p[3], p[4], p[5], p[7], " false")
            else :
                p[0] = "{} {} {} {} {} {}".format(p[1], p[2], p[3], p[4], p[5], p[7], " true")
  
    def p_term_steamid(self,p):
          '''playerid : STEAMIDPREFIX NUMBER ELLIPSIS NUMBER ELLIPSIS NUMBER
                        | BOT'''
          if len(p) > 2:
                steamid64 = (int(p[2]) << 56) | (1 << 52) | (1 << 32) | (int(p[6]) << 1) | int(p[4])

                p[0] = str(steamid64)

          else:
                p[0] = p[1]

    def p_term_player(self,p):
            '''pterm : NAME LOWER playerid UPPER TEAMQ
                      | NAME LOWER playerid UPPER DQUOTE'''
            if len(p[5]) > 2:
              p[0]= (p[1], p[3], p[5])
            else:
              p[0]= (p[1], p[3], None)


    def p_term_round_messages(self,p):
          '''expression : ROUND_START
                          | ROUND_END 
                          | ROUND_SPAWN'''
          p[0] = p[1]


    def p_error(self,p):
            print("Syntax error in input!", p)
            pass
    
