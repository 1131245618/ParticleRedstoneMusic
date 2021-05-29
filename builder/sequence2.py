from builder import sequence

outputFolder = '_seq'

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

    def makeCmd(self, log=False, loopCmd=''):
        # self.fixSeq()
        self.clearCmd()

        # 测试
        if log:
            doc = open(f'log.txt', 'w', encoding='utf-8')
            for item in self:
                doc.write(f'tick: {item.tick}' + '\n')
                doc.write('\n'.join(['  ' + s for s in item.cmds]) + '\n')

        lastTick = 0
        for item in self:
            currentTick = item.tick

            # 填充空帧
            if currentTick - lastTick > 1:
                for i in range(lastTick+1, currentTick):
                    self.buildCmd(
                        i, f'gamerule gameLoopFunction {outputFolder}:{i+1}' + '\n' + loopCmd)

            # 写当前帧
            cmdStr = '\n'.join(
                item.cmds) + f'\ngamerule gameLoopFunction {outputFolder}:{currentTick+1}' + '\n' + loopCmd
            self.buildCmd(currentTick, cmdStr)
            lastTick = currentTick
        self.buildCmd(
            lastTick+1, f'\ngamerule gameLoopFunction {outputFolder}:999999')
