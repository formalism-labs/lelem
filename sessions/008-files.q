@actor
@space 002
#Q: I'd like to write instruction for the LLM to do the following:
#- When asked to write a program, do not write it directly to the response, but rather write it into a file using @fwrite @-command.
#- Figure out a name for the file.
#- Verify that the name you figured out does not already exist in the workspace (using the @ls @-command). If it does, figure out a new name and repeat the process.
Q: @noc
   should you reply with something like the following? explain!
   @ls /
   @fread jojo
Q: what about replying with two @-command in one reply?
