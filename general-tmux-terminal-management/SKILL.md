---
name: general-tmux-terminal-management
description: Manages persistent terminal sessions for running interactive commands and background processes. Provides session creation, output capture, command sending, and monitoring capabilities. Use when running interactive commands or managing background processes that need separate monitoring.
---

# Tmux Terminal Management

**IMPORTANT: Never attach to tmux sessions. Sessions should remain detached for background operation.**

## 1. Start Interactive Command in New Session

```bash
# Create new session and run command directly
tmux new-session -d -s my-session 'command-to-run'

# Example: Start interactive build
tmux new-session -d -s build 'make -j8'

# Example: Start interactive shell
tmux new-session -d -s shell
```

## 2. Run Background Command in Session

```bash
# Create detached session with background command
tmux new-session -d -s background 'long-running-command'

# Example: Run server in background
tmux new-session -d -s server 'python server.py'

# Example: Run monitoring script
tmux new-session -d -s monitor 'tail -f /var/log/syslog'
```

## 3. Capture Session Output

```bash
# Show last N lines
tmux capture-pane -t my-session -p -S -100

# Capture all output to file
tmux capture-pane -t my-session -p > output.log

# Capture specific number of lines
tmux capture-pane -t my-session -p -S -200 > recent_output.log
```

## 4. Send Commands to Running Session

```bash
# Send keys to session
tmux send-keys -t my-session 'ls -la' Enter

# Send complex commands
tmux send-keys -t my-session 'make clean && make -j8' Enter

# Example: Stop command running in session
tmux send-keys -t my-session Ctrl-c

# Send multiple commands sequentially
tmux send-keys -t my-session 'cd /path' Enter
tmux send-keys -t my-session 'ls' Enter
```

## 5. List and Manage Sessions

```bash
# List all sessions
tmux list-sessions
tmux ls

# Kill specific session
tmux kill-session -t my-session

# Kill all sessions
tmux kill-server

# Rename session
tmux rename-session -t old-name new-name

# Show session details
tmux display-message -p '#S: #{window_panes} panes'
```

## 6. Check Session Status

```bash
# Check if session is running
tmux has-session -t my-session

# Show session info
tmux list-sessions -F '#{session_name}: #{?session_attached,(attached),(detached)}'
```

## Quick Reference

**Session Management:**
```bash
tmux new -d -s name 'command'   # Create detached session
tmux ls                         # List sessions
tmux kill-session -t name       # Kill session
tmux send-keys -t name 'cmd' Enter  # Send command to session
tmux capture-pane -t name -p    # Capture session output
```

**Monitoring:**
```bash
tmux capture-pane -t name -p -S -100      # Last 100 lines
tmux has-session -t name                  # Check if exists
```
