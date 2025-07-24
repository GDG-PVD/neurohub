#!/bin/bash
# Real-time monitoring script for workshop instructors

APP_NAME="${1:-neurohub-workshop}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear
echo -e "${BLUE}🎓 NeuroHub Workshop Monitor${NC}"
echo "============================"
echo ""

# Function to show stats
show_stats() {
    echo -e "${GREEN}📊 Current Status:${NC}"
    fly status -a "$APP_NAME" | grep -E "Instances|Memory|CPU"
    echo ""
}

# Function to count recent requests
count_requests() {
    echo -e "${YELLOW}📈 Recent Activity (last 5 min):${NC}"
    fly logs -a "$APP_NAME" --limit 1000 | grep -E "GET|POST" | tail -20
    echo ""
    echo -n "Total requests: "
    fly logs -a "$APP_NAME" --limit 1000 | grep -E "GET|POST" | wc -l
    echo ""
}

# Main monitoring loop
while true; do
    clear
    echo -e "${BLUE}🎓 NeuroHub Workshop Monitor${NC}"
    echo "============================"
    echo "App: $APP_NAME"
    echo "Time: $(date)"
    echo ""
    
    show_stats
    count_requests
    
    echo -e "${GREEN}Commands:${NC}"
    echo "  r - Restart app"
    echo "  l - Show live logs"
    echo "  s - Scale up/down"
    echo "  q - Quit"
    echo ""
    echo "Auto-refresh in 30s..."
    
    # Read input with timeout
    read -t 30 -n 1 input
    
    case $input in
        r)
            echo "Restarting app..."
            fly apps restart "$APP_NAME"
            sleep 5
            ;;
        l)
            echo "Showing live logs (Ctrl+C to return)..."
            fly logs -a "$APP_NAME"
            ;;
        s)
            echo "Current scale:"
            fly scale show -a "$APP_NAME"
            echo ""
            read -p "New instance count (1-3): " count
            fly scale count "$count" -a "$APP_NAME"
            ;;
        q)
            echo "Goodbye! 👋"
            exit 0
            ;;
    esac
done