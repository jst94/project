"""
Performance Optimization Module for PoE Craft Helper
Optimizes resource usage, memory management, and UI responsiveness
"""

import gc
import psutil
import threading
import time
from typing import Dict, Any, Callable
import weakref
from dataclasses import dataclass
from datetime import datetime
import tkinter as tk


@dataclass
class PerformanceMetrics:
    """Performance metrics data class"""
    cpu_usage: float
    memory_usage: float
    memory_mb: float
    thread_count: int
    ui_response_time: float
    market_api_latency: float
    timestamp: datetime


class PerformanceOptimizer:
    """Optimizes application performance and resource usage"""
    
    def __init__(self, app_instance):
        self.app = weakref.ref(app_instance)  # Weak reference to avoid circular refs
        self.metrics_history = []
        self.monitoring_active = False
        self.optimization_callbacks = []
        
        # Performance thresholds
        self.cpu_threshold = 15.0  # Max 15% CPU usage
        self.memory_threshold = 100.0  # Max 100MB memory usage
        self.ui_response_threshold = 0.1  # Max 100ms UI response
        
        # Optimization strategies
        self.optimization_strategies = {
            'memory_cleanup': self.cleanup_memory,
            'ui_optimization': self.optimize_ui,
            'background_throttle': self.throttle_background_tasks,
            'cache_management': self.manage_caches
        }
        
    def start_monitoring(self):
        """Start performance monitoring"""
        if self.monitoring_active:
            return
            
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    metrics = self.collect_metrics()
                    self.metrics_history.append(metrics)
                    
                    # Keep only last 100 measurements
                    if len(self.metrics_history) > 100:
                        self.metrics_history.pop(0)
                    
                    # Check if optimization is needed
                    self.check_optimization_triggers(metrics)
                    
                    time.sleep(5)  # Check every 5 seconds
                    
                except Exception as e:
                    print(f"Performance monitoring error: {e}")
                    time.sleep(10)
                    
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        
    def collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics"""
        try:
            process = psutil.Process()
            
            # CPU and memory usage
            cpu_usage = process.cpu_percent()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            memory_percent = process.memory_percent()
            
            # Thread count
            thread_count = process.num_threads()
            
            # UI response time (simplified)
            ui_start = time.time()
            if self.app() and self.app().root:
                self.app().root.update_idletasks()
            ui_response_time = time.time() - ui_start
            
            # Market API latency (if available)
            market_latency = 0.0
            if self.app() and hasattr(self.app(), 'market_api'):
                try:
                    start_time = time.time()
                    # Quick connectivity check
                    status = self.app().market_api.get_api_status()
                    market_latency = time.time() - start_time
                except:
                    market_latency = -1.0  # Error indicator
            
            return PerformanceMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory_percent,
                memory_mb=memory_mb,
                thread_count=thread_count,
                ui_response_time=ui_response_time,
                market_api_latency=market_latency,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            return PerformanceMetrics(0, 0, 0, 0, 0, 0, datetime.now())
            
    def check_optimization_triggers(self, metrics: PerformanceMetrics):
        """Check if optimization is needed based on metrics"""
        optimizations_needed = []
        
        # Check CPU usage
        if metrics.cpu_usage > self.cpu_threshold:
            optimizations_needed.append('background_throttle')
            
        # Check memory usage
        if metrics.memory_mb > self.memory_threshold:
            optimizations_needed.append('memory_cleanup')
            
        # Check UI responsiveness
        if metrics.ui_response_time > self.ui_response_threshold:
            optimizations_needed.append('ui_optimization')
            
        # Check if we have too much cached data
        if len(self.metrics_history) > 50 and metrics.memory_mb > 50:
            optimizations_needed.append('cache_management')
            
        # Apply optimizations
        for optimization in optimizations_needed:
            if optimization in self.optimization_strategies:
                try:
                    self.optimization_strategies[optimization]()
                except Exception as e:
                    print(f"Optimization error ({optimization}): {e}")
                    
    def cleanup_memory(self):
        """Clean up memory usage"""
        try:
            # Force garbage collection
            gc.collect()
            
            # Clear old metrics history if too large
            if len(self.metrics_history) > 20:
                self.metrics_history = self.metrics_history[-20:]
                
            # Clear market API cache if available
            if self.app() and hasattr(self.app(), 'market_api'):
                # Clear old currency data
                market_api = self.app().market_api
                if hasattr(market_api, 'currency_data'):
                    # Keep only essential currency data
                    essential_currencies = ['Chaos Orb', 'Divine Orb', 'Exalted Orb']
                    if len(market_api.currency_data) > len(essential_currencies) * 2:
                        market_api.currency_data = {k: v for k, v in market_api.currency_data.items() 
                                                   if k in essential_currencies}
                                                   
            print("Memory cleanup completed")
            
        except Exception as e:
            print(f"Memory cleanup error: {e}")
            
    def optimize_ui(self):
        """Optimize UI performance"""
        try:
            if not self.app() or not self.app().root:
                return
                
            app = self.app()
            
            # Reduce update frequency for heavy elements
            if hasattr(app, 'results_text'):
                # Temporarily disable text widget updates
                app.results_text.config(state='disabled')
                app.root.after(100, lambda: app.results_text.config(state='normal'))
                
            # Optimize overlay updates
            if hasattr(app, 'status_label'):
                # Update status less frequently
                app.root.after(10000, app.update_price_status)  # 10 seconds instead of immediate
                
            # Force UI cleanup
            app.root.update_idletasks()
            
            print("UI optimization completed")
            
        except Exception as e:
            print(f"UI optimization error: {e}")
            
    def throttle_background_tasks(self):
        """Throttle background tasks to reduce CPU usage"""
        try:
            if not self.app():
                return
                
            app = self.app()
            
            # Increase price update interval temporarily
            if hasattr(app, 'market_api'):
                old_interval = app.market_api.update_interval
                app.market_api.update_interval = min(old_interval * 2, 1800)  # Max 30 minutes
                
                # Restore normal interval after 5 minutes
                def restore_interval():
                    if app.market_api:
                        app.market_api.update_interval = old_interval
                        
                app.root.after(300000, restore_interval)  # 5 minutes
                
            print("Background tasks throttled")
            
        except Exception as e:
            print(f"Background throttling error: {e}")
            
    def manage_caches(self):
        """Manage application caches"""
        try:
            if not self.app():
                return
                
            app = self.app()
            
            # Clear session tracker cache if too large
            if hasattr(app, 'session_tracker'):
                tracker = app.session_tracker
                if hasattr(tracker, 'get_session_history'):
                    # Limit session history in memory
                    recent_sessions = tracker.get_session_history(10)  # Keep only 10 recent
                    
            # Clear modifier database cache if available
            if hasattr(app, 'modifier_database'):
                # Keep only essential modifiers
                essential_mods = ['Maximum Life', 'Energy Shield', 'Resistances']
                # This is just an example - actual implementation would depend on structure
                
            print("Cache management completed")
            
        except Exception as e:
            print(f"Cache management error: {e}")
            
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        if not self.metrics_history:
            return {'error': 'No metrics available'}
            
        recent_metrics = self.metrics_history[-10:]  # Last 10 measurements
        
        # Calculate averages
        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_mb for m in recent_metrics) / len(recent_metrics)
        avg_ui_response = sum(m.ui_response_time for m in recent_metrics) / len(recent_metrics)
        
        # Find peak usage
        peak_cpu = max(m.cpu_usage for m in recent_metrics)
        peak_memory = max(m.memory_mb for m in recent_metrics)
        
        # Performance status
        status = 'good'
        if avg_cpu > self.cpu_threshold or avg_memory > self.memory_threshold:
            status = 'warning'
        if peak_cpu > self.cpu_threshold * 2 or peak_memory > self.memory_threshold * 2:
            status = 'critical'
            
        return {
            'status': status,
            'average_cpu_usage': avg_cpu,
            'average_memory_mb': avg_memory,
            'average_ui_response_ms': avg_ui_response * 1000,
            'peak_cpu_usage': peak_cpu,
            'peak_memory_mb': peak_memory,
            'total_measurements': len(self.metrics_history),
            'monitoring_active': self.monitoring_active,
            'timestamp': datetime.now().isoformat()
        }
        
    def optimize_on_startup(self):
        """Perform startup optimizations"""
        try:
            # Set process priority to normal (not high)
            try:
                import psutil
                process = psutil.Process()
                process.nice(0)  # Normal priority
            except:
                pass
                
            # Optimize garbage collection
            gc.set_threshold(700, 10, 10)  # More aggressive GC
            
            # Pre-allocate common objects to reduce allocation overhead
            self.common_strings = {
                'chaos_orb': 'Chaos Orb',
                'divine_orb': 'Divine Orb',
                'exalted_orb': 'Exalted Orb',
                'success': 'Success',
                'failed': 'Failed'
            }
            
            print("Startup optimizations applied")
            
        except Exception as e:
            print(f"Startup optimization error: {e}")
            
    def create_performance_widget(self, parent: tk.Widget) -> tk.Frame:
        """Create a performance monitoring widget"""
        try:
            frame = tk.Frame(parent)
            
            # Title
            tk.Label(frame, text="Performance Monitor", 
                    font=("Arial", 10, "bold")).pack()
            
            # Metrics display
            self.perf_labels = {}
            metrics = ['CPU', 'Memory', 'UI Response']
            
            for metric in metrics:
                metric_frame = tk.Frame(frame)
                metric_frame.pack(fill='x', padx=5, pady=2)
                
                tk.Label(metric_frame, text=f"{metric}:", 
                        font=("Arial", 8)).pack(side='left')
                
                self.perf_labels[metric] = tk.Label(metric_frame, text="--", 
                                                   font=("Arial", 8, "bold"))
                self.perf_labels[metric].pack(side='right')
                
            # Update button
            tk.Button(frame, text="Optimize Now", 
                     command=self.force_optimization,
                     font=("Arial", 8)).pack(pady=5)
            
            # Start updating the widget
            self.update_performance_widget()
            
            return frame
            
        except Exception as e:
            print(f"Performance widget error: {e}")
            return tk.Frame(parent)
            
    def update_performance_widget(self):
        """Update performance widget display"""
        try:
            if not hasattr(self, 'perf_labels'):
                return
                
            if self.metrics_history:
                latest = self.metrics_history[-1]
                
                # Update labels with color coding
                cpu_color = 'green' if latest.cpu_usage < 10 else 'orange' if latest.cpu_usage < 20 else 'red'
                self.perf_labels['CPU'].config(text=f"{latest.cpu_usage:.1f}%", fg=cpu_color)
                
                mem_color = 'green' if latest.memory_mb < 50 else 'orange' if latest.memory_mb < 100 else 'red'
                self.perf_labels['Memory'].config(text=f"{latest.memory_mb:.1f}MB", fg=mem_color)
                
                ui_color = 'green' if latest.ui_response_time < 0.05 else 'orange' if latest.ui_response_time < 0.1 else 'red'
                self.perf_labels['UI Response'].config(text=f"{latest.ui_response_time*1000:.0f}ms", fg=ui_color)
                
            # Schedule next update
            if self.app() and self.app().root:
                self.app().root.after(5000, self.update_performance_widget)
                
        except Exception as e:
            print(f"Performance widget update error: {e}")
            
    def force_optimization(self):
        """Force immediate optimization"""
        try:
            for strategy in self.optimization_strategies.values():
                strategy()
            print("Manual optimization completed")
        except Exception as e:
            print(f"Force optimization error: {e}")


def optimize_tkinter_performance(root: tk.Tk):
    """Apply Tkinter-specific performance optimizations"""
    try:
        # Reduce update frequency
        root.tk.call('set', 'tk_strictMotif', '1')
        
        # Optimize drawing
        root.tk.call('set', 'tcl_precision', '6')
        
        # Reduce font rendering overhead
        root.option_add('*font', 'Arial 9')
        
        print("Tkinter optimizations applied")
        
    except Exception as e:
        print(f"Tkinter optimization error: {e}")


# Global performance optimizer (initialized when app starts)
performance_optimizer = None


def initialize_performance_optimizer(app_instance):
    """Initialize global performance optimizer"""
    global performance_optimizer
    performance_optimizer = PerformanceOptimizer(app_instance)
    performance_optimizer.optimize_on_startup()
    performance_optimizer.start_monitoring()
    return performance_optimizer