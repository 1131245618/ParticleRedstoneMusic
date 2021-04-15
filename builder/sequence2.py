from builder import sequence


class Seq2(sequence.Seq):
    def makeNonemptyCmd(self, log=False):

        self.clearCmd()

        if log:
            doc = open('log.txt', 'w', encoding='utf-8')
            for item in self:
                doc.write(f'tick: {item.tick}' + '\n')
                doc.write('\n'.join(['  ' + s for s in item.cmds]) + '\n')

        for item in self:
            currentTick = item.tick

            if item.cmds:
                cmdStr = '\n'.join(item.cmds)
                self.buildCmd(currentTick, cmdStr)
