```
----------------------------------------------------------------------------------

                 Server                           client                      remote AI
        waiting for client to plug in                |                            |           
                   |<~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|tcp connect                 |
                   |                                 |send: player name           |
                time up                              |                            |
                   |                                 |                            |
            Initialize players                       |                            |
          found duplicated name                      |                            |
                   |                                 |                            |
           new_name|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                            |
                   |                                 |                            |
            run tournament                           |                            |
        other players playing                        |                            |
                   |                                 |                            |
                ------------------------------------------------------------------
                                                
                                        ......Best of N Phase......
                                                
                ------------------------------------------------------------------
                   |                               reset                          |
                ...|                                 |                            |
    tournament over|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                            |
                   |                            show outcome                      |

----------------------------------------------------------------------------------

Best of N Phase:
----------------------------------------------------------------------------------
                 Server                           client                      remote AI
                    ---------------------------------------------------------------
                                                
                                          ......Game PHASE......
                                             
                                ......UNTIL N GAMES HAVE BEEN PLAYED......
                                                
                    ---------------------------------------------------------------
      Best N result|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                            |
----------------------------------------------------------------------------------

Game Phase:
----------------------------------------------------------------------------------
                 Server                           client                      remote AI
         game start|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                            |
                   |                         Initialize a board                   |
                    ---------------------------------------------------------------
                                                
                                     ......PLACEMENT PHASE......
                                             
                        ......UNTIL BOTH PLAYERS HAVE PLACED TWO WORKERS......
                                                
                    ---------------------------------------------------------------
                    ---------------------------------------------------------------
                                                
                                     ......MOVE_BUILD PHASE......
                                             
                        ......UNTIL BOTH PLAYERS HAVE PLACED TWO WORKERS......
                                                
                    ---------------------------------------------------------------
          game_over|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                            |
----------------------------------------------------------------------------------

Placement Phase
(Or Timeout Case/Invalid Command Case if server time out/received Invalid command):
------------------------------------------------------------------------------------
                 Server                           client                      remote AI
  placement request|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                            |
                   |                       place worker on board                  |
                   |      board and placement request|--------------------------->|
                   |                                 |<---------------------------|wid_posn
                   |                       place worker on board                  |
                   |<~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|wid_posn                    |
------------------------------------------------------------------------------------

Move_build Phase
(Or Timeout Case/Invalid Command Case if server time out/received Invalid command):
------------------------------------------------------------------------------------
move_build request|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                             |
                   |                      move and build on board                 |
                   |    board and move_build request|---------------------------->|
                   |                                |<----------------------------|wid_move_build_dir               |                             |
                   |                      move and build on board                 | 
                   |<~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|wid_move_build_dir          |

IF client can not reply to server before server time out, following indicate what will happen
------------------------------------------------------------------------------------

Timeout Case:
(request can be interpreted as either placement request or move_build request)
------------------------------------------------------------------------------------
                 Server                           client                      remote AI
            request|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                            |
                   |                   perform action on the board                |
                   |                board and request|--------------------------->|
                   |                              waiting                         |
                time out                             |                            |
     remove connect with the client                  |                            |
------------------------------------------------------------------------------------

Invalid Command Case:
(request can be interpreted as either placement request or move_build request)
------------------------------------------------------------------------------------
                 Server                           client                      remote AI
  placement request|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                            |
                   |                       place worker on board                  |
                   |      board and placement request|--------------------------->|
                   |                                 |<---------------------------|wid_posn
                   |                       place worker on board                  |
                   |<~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|wid_posn                    |
        Received invalid command                     |                            |
  game_over & e_msg|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>|                            |          
------------------------------------------------------------------------------------
```

```
The message formats are as follows:

Message             | Format
------------------------------------------------------------------------------------
player name         | {"type": "Name", "content": name}

new name            | {"type": "Name", "content": name}

game start          | {"type": "Start", "content": Null}

placement request   | {"type": "placement", "content": [wid, posn]}

wid_posn            | {"type": "placement", "content": [wid, posn]} 
                      where wid is int and posn is tuple of two int

move_build request  | {"type": "move_build", "content": Null}

wid_move_build_dir  | {"type": "move_build", "content": [wid, move_dir, build_dir]}
                      where move_dir and build_dir is str like "North", "South" etc and
                      build_dir can be Null if move_dir is the winning move.

game_start          | {"type": "game_start", "content": Null}

game_over           | {"type": "game_over", "content": won}
                      where won is a boolean represent if client won this game

Best N result       | {"type": "best_n_over", "content": won}
                      where won is a boolean represent if client won this game
                      
tournament over     | {"type": "tournament_over", "content": [won, game_history]}
                      where won is a boolean represent if client won this game
                      and game_history is a array of game which is a tuple containing
                      two the winner name and the loser name

e_msg               | {"type": "error_msg", "content": error message}

```
