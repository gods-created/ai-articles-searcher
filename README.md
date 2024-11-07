How to launch application?
Steps:
1. Fulling .env params
2. export $(cat .env | xargs) - install environment
3. python configs/init.py - for creating secrets and tune database
4. python main.py - launch application
5. Open http://0.0.0.0:8001/docs and testing
