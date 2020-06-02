from Game.GameMVC import Game

game = Game(manual=False)
model, view, controller = game.getMVC()

for i in range(1000000):

    print('Turn {}'.format(i+1))
    controller.runTurn()
    if i % 1000 == 0:
        model.player.actionSelector.comeOutDecisionCore.dp.save_on_file()
        a = [x > 0 for x in model.player.actionSelector.comeOutDecisionCore.dp.occurrence_map]
        print(model.player.actionSelector.comeOutDecisionCore.dp.occurrence_map[a])
    # if model.player.cash <= 0:
    #     break
