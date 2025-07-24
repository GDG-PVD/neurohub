#!/bin/bash
# Script to push the a2a-demo to the neurohub repository

echo "🚀 Pushing to NeuroHub repository..."

# Option 1: Force push (if you want to replace everything in the remote)
echo "Option 1: Force push (replaces remote content)"
echo "git push -f origin main"
echo ""

# Option 2: Pull and merge (if you want to keep remote content)
echo "Option 2: Pull first, then push"
echo "git pull origin main --allow-unrelated-histories"
echo "git push origin main"
echo ""

# Option 3: Push to a new branch
echo "Option 3: Push to a new branch"
echo "git push origin main:workshop-materials"
echo ""

echo "Which option would you like to use?"
echo "1) Force push (replaces everything)"
echo "2) Merge with existing content"
echo "3) Push to new branch 'workshop-materials'"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "⚠️  This will replace all content in the remote repository!"
        read -p "Are you sure? (y/n): " confirm
        if [ "$confirm" = "y" ]; then
            git push -f origin main
            echo "✅ Force pushed to main branch"
        fi
        ;;
    2)
        echo "Pulling remote content..."
        git pull origin main --allow-unrelated-histories
        echo "Now pushing merged content..."
        git push origin main
        echo "✅ Pushed merged content to main branch"
        ;;
    3)
        git push origin main:workshop-materials
        echo "✅ Pushed to workshop-materials branch"
        echo "You can create a PR on GitHub to merge into main"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Done! Visit https://github.com/GDG-PVD/neurohub"