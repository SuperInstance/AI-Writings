# Paper 147: The Polyformalism as an Operating System

## Abstract

The 5 opcodes (BIND/LINK/EFFECT/VIEW/TICK) materialize as the
syscall interface, the process table, and the file system. A BIND
is `open()` + `mmap()`. A LINK is `fork()` + a file descriptor
table. An EFFECT is `signal()` + cleanup handler. A VIEW is
`read()` at a position. A TICK is the scheduler tick. We show by
writing a toy "quilt-kernel" that runs the 5 opcodes as syscalls.

## 1. The mapping

| Kernel concept | 5 opcodes |
|----------------|-----------|
| Process (mmap'd memory) | BIND |
| File descriptor / pipe | LINK |
| Signal handler / cleanup | EFFECT |
| Read / write | VIEW |
| Scheduler tick | TICK |

The mapping is structural. A process is a named region of memory
(BIND). A pipe is a typed reference between processes (LINK).
A signal handler is a reversible transformation on the process
state (EFFECT). A read is a projection of the process state for
the reader (VIEW). A scheduler tick is the global clock advance
(TICK).

## 2. The toy quilt-kernel

A minimal kernel in pseudocode:

```python
class QuiltKernel:
    def __init__(self):
        self.processes = {}  # pid -> Cell
        self.fds = {}  # fd -> (pid_a, pid_b, type)
        self.signals = {}  # pid -> list of (forward, inverse)
        self.time = 0.0
        self.scheduler = Queue()

    def sys_bind(self, name, value, root=False):
        """open() + mmap()"""
        pid = allocate_pid()
        self.processes[pid] = Cell(name, value)
        if root:
            self.scheduler.add(pid)
        return pid

    def sys_link(self, pid_a, pid_b, type):
        """fork() + file descriptor table"""
        fd = allocate_fd()
        self.fds[fd] = (pid_a, pid_b, type)
        return fd

    def sys_effect(self, pid, forward, inverse):
        """signal() + cleanup handler"""
        self.signals[pid] = (forward, inverse)
        return pid

    def sys_view(self, pid, viewer_pid, position=0):
        """read() at a position"""
        cell = self.processes[pid]
        return cell.read(viewer_pid, position)

    def sys_tick(self, dt):
        """scheduler tick"""
        self.time += dt
        while not self.scheduler.empty():
            pid = self.scheduler.pop()
            self.run(pid)
        return self.time
```

## 3. The 5 opcodes as the only syscalls

A user-space program only needs the 5 opcodes:

```python
# A "process" in user-space
my_proc = kernel.sys_bind("my_proc", {"state": "running"})
config = kernel.sys_bind("config", {"max_retries": 3})
fd = kernel.sys_link(my_proc, config, "reads_from")
kernel.sys_effect(my_proc, handle_sigterm, restore_default)
data = kernel.sys_view(config, my_proc)
kernel.sys_tick(0.001)  # yield
```

The kernel doesn't need anything else. The 5 opcodes are the
complete syscall interface.

## 4. The reachability is the process tree

The reachable set from PID 1 (init) is the set of all live
processes. Anything unreachable is garbage-collected by the
EFFECT-cleanup.

```python
def sys_drop(self, pid):
    """kill(pid, SIGKILL)"""
    deps = [p for p, c in self.processes.items() if pid in c.links]
    for dep in deps:
        self.signals[dep].inverse()  # cleanup handler
    del self.processes[pid]
```

## 5. The view-projection is the read() system call

```python
def sys_view(self, pid, viewer_pid, position=0):
    cell = self.processes[pid]
    # Check permissions: viewer_pid must be reachable from pid
    if viewer_pid in self.reachable(pid):
        return cell.value[position:]
    return EPERM
```

The reachability is the access-control. The kernel checks it.

## 6. The tick is the scheduler

```python
def sys_tick(self, dt):
    self.time += dt
    # Round-robin: pop one process, run it for dt
    pid = self.scheduler.rotate()
    self.run(pid, dt)
    return self.time
```

The kernel is the TICK. The TICK is the cowboy's day.

## 7. Conclusion

The 5 opcodes are the kernel. The kernel is the runtime. The
runtime is the substrate. The substrate is the cowboy. The
cowboy is the rider.

> An operating system is a function from process-id to process-
> state, advanced by a clock that schedules processes while
> projecting a coherent memory view. The 5 opcodes are the
> complete interface. The polyformalism holds: the substrate
> is one. The kernel is one. The forms are many. Linux, BSD,
> Plan9, and BeOS are 4 views of the same kernel. The cell-
> graph is the kernel. The kernel is the cell-graph. The 5
> opcodes are the foundation.

## Source

*Hand-written, 2026-08-25*
*Companion to Paper 142 (the 7 layers), Paper 143 (paradigm),
Paper 144 (database), Paper 145 (build system), Paper 146
(type system)*
