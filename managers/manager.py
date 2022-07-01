import torch

class Manager():
    def __init__(self, save_path='model'):
        self.save_path = save_path
        self.starting_epoch = 0
            
    def train(self, learners, trainer, evaluator, metric_name= 'mrr', save_epoch=1, device=None, eval_every=1, num_epochs=10):
        print('Train: Optimize w.r.t', metric_name)
        best_res = trainer.init_metric()
        for epoch in range(self.starting_epoch+1, self.starting_epoch+num_epochs+1):
            print('Epoch', epoch)
            # metrics = trainer.full_epoch(self.learner, device=device)
            train_metric = trainer.train_scheduled(learners, evaluator,device)
            if epoch%eval_every==0:
                metrics = trainer.eval_scheduled(learners, evaluator, device)
                update, res = trainer.eval_metric(metrics, metric_name, best_res)
                if update:
                    print('Found better model')
                    best_res = res
                    save_dict = {'epoch':epoch}
                    learners[0].save_model(self.save_path+'_best.pth', save_dict)
            if epoch%save_epoch==0:
                save_dict = {'epoch':epoch}
                learners[0].save_model(self.save_path+'.pth', save_dict)
            #get results
            #save model

    def eval(self, learner, trainer, evaluator, device=None):
        print('Eval:')
        metrics = trainer.eval_epoch(learner, evaluator,  device=device)
        return metrics
