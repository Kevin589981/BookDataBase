// 简单的调试脚本，检查Vue应用是否正确加载
console.log('Debug script loaded');

// 检查Vue是否已挂载
setTimeout(() => {
    const app = document.getElementById('app');
    console.log('App element:', app);
    console.log('App innerHTML:', app ? app.innerHTML : 'App element not found');
    
    // 检查是否有Vue实例
    if (window.Vue) {
        console.log('Vue is available:', window.Vue);
    } else {
        console.log('Vue is not available on window object');
    }
    
    // 检查是否有错误
    if (window.console && window.console.error) {
        const originalError = window.console.error;
        window.console.error = function(...args) {
            console.log('Console error detected:', args);
            originalError.apply(console, args);
        };
    }
}, 1000);