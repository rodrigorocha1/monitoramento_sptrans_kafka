from src.controllers.dashboard_controller import DashboardController

if __name__ == '__main__':
    dc = DashboardController()
    print(dc.obter_nome_linha('4027-41')[0][0])