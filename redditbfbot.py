import praw

def compileComment(comment):
     
     #char limit
     cells = [0] * len(comment)
     
     #utility variables
     i,j,k = 0,0,0
     loop = 0
     flag = False
     
     #initial values
     cellptr = 0
     charlist = []
     output = ""
     
     while (i < len(comment)):
     
          #increment value at that point 
          if comment[i] == '+':
               cells[cellptr] += 1

          #decrement value at that point
          if comment[i] == '-':
               cells[cellptr] -= 1
               
          #move pointer to the right,  wrap around if we hit the end
          if comment[i] == '>':
               cellptr += 1
               if cellptr == len(cells) - 1:
                   cellptr = 0
                   
          #move pointer to the left, wrap around if we hit the start
          if comment[i] == '<':
               cellptr -= 1
               if cellptr < 0:
                   cellptr = len(cells) - 1

          #cast int at the pointer location to a char
          if comment[i] == '.':
               try:
                    charlist.insert(k, chr(cells[cellptr]))
                    k += 1
               except ValueError:
                    flag = 1
          
          if comment[i] == '[':
               #if were done looping, skip past the loop, without executing in between chars
               if cells[cellptr] == 0:
                    loop = 1
                    while (not (loop == 0 and comment[i] == ']')):
                         i += 1
                         if comment[i] == '[':
                              loop += 1
                         elif comment[i] == ']':
                              loop -= 1
                         
               #if we're not done, decrement the loop count, and continue     
               else:
                    pass

     
          if comment[i] == ']':
                              
               #if we're done looping, continue
               if cells[cellptr] == 0:
                    pass

               #otherwise, jump back to corresponding '['
               else:
                    loop = 1
                    while (not (loop == 0 and comment[i] == '[')):
                         i -= 1
                         if comment[i] == ']':
                              loop += 1
                         elif comment[i] == '[':
                              loop -= 1
                    
               
               
          #keeps track of which char we're on
          i += 1
          
     if flag:
          output = "1"
          
     output = "".join(charlist)
     return output


def main():

    #establish connection 
    reddit = praw.Reddit(client_id = 'NA',
                         client_secret = "NA",
                         password = 'NA',
                         user_agent = 'Brainfuck compiler by /u/dav051498',
                         username = 'BrainFuckCompileBot')
     
    goodboy = "good bot"
    badboy = "bad bot"
    #for each new mention  
    for mention in reddit.inbox.unread():
         #base responses to feedback          
         if goodboy in mention.body.lower():
            mention.reply("no u")
            mention.upvote()
            mention.mark_read()
            
         elif badboy in mention.body.lower():
            mention.reply("Bots have feelings too :(")   
            mention.mark_read()
         #if its not feedback, try to compile it   
         else: 
            output = compileComment(mention.body)
            mention.reply(output)
            mention.mark_read()
         
    
if __name__ == "__main__": main()
