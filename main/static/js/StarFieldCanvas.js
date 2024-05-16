var StarFieldCanvas = function (t) {
    var s = {};

    function i(e) {
        if (s[e]) return s[e].exports;
        var a = s[e] = {
            i: e,
            l: !1,
            exports: {}
        };
        return t[e].call(a.exports, a, a.exports, i), a.l = !0, a.exports
    }
    return i.m = t, i.c = s, i.d = function (t, s, e) {
        i.o(t, s) || Object.defineProperty(t, s, {
            enumerable: !0,
            get: e
        })
    }, i.r = function (t) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(t, "__esModule", {
            value: !0
        })
    }, i.t = function (t, s) {
        if (1 & s && (t = i(t)), 8 & s) return t;
        if (4 & s && "object" == typeof t && t && t.__esModule) return t;
        var e = Object.create(null);
        if (i.r(e), Object.defineProperty(e, "default", {
                enumerable: !0,
                value: t
            }), 2 & s && "string" != typeof t)
            for (var a in t) i.d(e, a, function (s) {
                return t[s]
            }.bind(null, a));
        return e
    }, i.n = function (t) {
        var s = t && t.__esModule ? function () {
            return t.default
        } : function () {
            return t
        };
        return i.d(s, "a", s), s
    }, i.o = function (t, s) {
        return Object.prototype.hasOwnProperty.call(t, s)
    }, i.p = "", i(i.s = 0)
}([function (t, s, i) {
    "use strict";
    i.r(s);
    class e {
        constructor() {
            this.animate = !1, this.frameReqId = 0, this.frameTasks = [], this.lastFrameTaskId = 0, this.loop = (t = 0) => {
                const s = this.frameTasks.length;
                for (let i = 0; i < s; i++) this.frameTasks[i].fn(t);
                this.frameReqId = requestAnimationFrame(this.loop)
            }, this.addTasks = this.addTasks.bind(this)
        }
        addTask(t) {
            return this.addTasks([t])[0]
        }
        addTasks(t) {
            const s = [];
            return 0 == t.length ? s : (t.forEach(t => {
                this.frameTasks.push({
                    id: this.lastFrameTaskId,
                    fn: t
                }), s.push(this.lastFrameTaskId), this.lastFrameTaskId++
            }), s)
        }
        deleteTask(t) {
            this.frameTasks = this.frameTasks.filter(s => s.id !== t)
        }
        start(t) {
            this.animate || (this.animate = !0, this.loop())
        }
        stop() {
            cancelAnimationFrame(this.frameReqId), this.animate = !1
        }
    }
    const a = (t, s, i, e, a) => (t - s) * (a - e) / (i - s) + e;
    var h = {
            r: 255,
            b: 255,
            g: 255
        },
        n = function () {
            function t(t) {
                this.x = 0, this.y = 0, this.z = 0, this.v = 0, this.radius = 0, this.lastX = 0, this.lastY = 0, this.splashLimitX = [0, 0], this.splashLimitY = [0, 0];
                var s = t.ctx,
                    i = t.W,
                    e = t.H,
                    a = t.hW,
                    n = t.hH,
                    o = t.minV,
                    r = t.maxV,
                    l = t.color,
                    f = t.glow,
                    c = t.trails,
                    u = t.addTasks;
                this.ctx = s, this.W = i, this.H = e, this.hW = a, this.hH = n, this.minV = o, this.maxV = r, this.glow = f, this.trails = c, this.color = l || h, this.splashLimitX = [-a, a], this.splashLimitY = [-n, n], this.addTasks = u, this.reset(!0)
            }
            return t.prototype.getInitialZ = function () {
                return 2 * (this.W > this.H ? this.H : this.W)
            }, t.prototype.draw = function (t, s) {
                this.z -= this.v, this.z <= 0 && this.reset();
                var i = this.W * (this.x / this.z) - t,
                    e = this.H * (this.y / this.z) - s,
                    h = this.getInitialZ(),
                    n = (1 - a(this.z, 0, h, 0, 1)) * this.radius,
                    o = Math.round(10 - a(this.z, 0, h, 0, 10)) / 10,
                    r = o / 4;
                this.trails && this.lastX !== this.x && (this.ctx.lineWidth = n, this.ctx.strokeStyle = "rgba(" + this.color.r + ", " + this.color.g + ", " + this.color.b + ", " + r + ")", this.ctx.beginPath(), this.ctx.moveTo(i, e), this.ctx.lineTo(this.lastX, this.lastY), this.ctx.stroke()), this.glow && (this.ctx.save(), this.ctx.shadowBlur = 5, this.ctx.shadowColor = "#FFF"), this.ctx.fillStyle = "rgb(" + this.color.r + ", " + this.color.g + ", " + this.color.b + ", " + o + ")", this.ctx.beginPath(), this.ctx.arc(i, e, n, 0, 2 * Math.PI), this.ctx.fill(), this.glow && this.ctx.restore(), this.lastX = i, this.lastY = e
            }, t.prototype.reset = function (t) {
                void 0 === t && (t = !1), this.x = Math.random() * this.W - this.hW, this.y = Math.random() * this.H - this.hH, this.v = Math.random() * (this.maxV - this.minV) + this.minV, this.radius = Number((2 * Math.random() + 1).toPrecision(3)), this.lastX = this.x, this.lastY = this.y, this.z = t ? Math.random() * this.getInitialZ() : this.getInitialZ()
            }, t
        }();
    i.d(s, "StarField", (function () {
        return o
    }));
    var o = function () {
        function t(t, s) {
            var i = this;
            if (void 0 === s && (s = {}), this.defaultMaxV = 5, this.defaultMinV = 2, this.defaultNumStars = 400, this.initialized = !1, this.canvasW = 0, this.canvasH = 0, this.canvasHalfW = 0, this.canvasHalfH = 0, this.offsetX = 0, this.offsetY = 0, this.offsetTX = 0, this.offsetTY = 0, this.stars = [], this.resizeTimeout = 0, !t) throw 'First argument "id" is required';
            this.color = s.color || h, this.glow = s.glow || !1, this.minV = s.minV || this.defaultMinV, this.maxV = s.maxV || this.defaultMaxV, this.numStars = this.defaultNumStars, this.trails = s.trails || !1, this.canvas = document.getElementById(t), this.ctx = this.canvas.getContext("2d");
            var a = this.canvas.getBoundingClientRect();
            this.canvasRectLeft = a.left, this.canvasRectTop = a.top, this.followContext = s.followContext || this.canvas, this.handleMouseMove = this.handleMouseMove.bind(this), this.engine = new e, this.engine.addTask(this.draw.bind(this)), window.addEventListener("blur", (function () {
                i.stop()
            })), window.addEventListener("focus", (function () {
                i.start()
            })), window.addEventListener("resize", (function () {
                clearTimeout(i.resizeTimeout), i.stop(), i.resizeTimeout = setTimeout((function () {
                    i.reset(), i.start()
                }), 500)
            })), this.numStars = s.numStars ? Math.abs(s.numStars) : this.defaultNumStars, this.setupCanvas(), this.generateStars(), this.initialized = !0, s.followMouse && this.setFollowMouse(!0)
        }
        return t.prototype.generateStars = function () {
            for (var t = 0; t < this.numStars; t++) this.stars.push(new n({
                ctx: this.ctx,
                W: this.canvasW,
                H: this.canvasH,
                hW: this.canvasHalfW,
                hH: this.canvasHalfH,
                minV: this.minV,
                maxV: this.maxV,
                color: this.color,
                glow: this.glow,
                trails: this.trails,
                addTasks: this.engine.addTasks
            }))
        }, t.prototype.setupCanvas = function () {
            var t = window.getComputedStyle(this.canvas);
            this.canvas.setAttribute("height", t.height), this.canvas.setAttribute("width", t.width), this.canvasH = this.canvas.height, this.canvasW = this.canvas.width, this.canvasHalfH = this.canvasH / 2, this.canvasHalfW = this.canvasW / 2, this.ctx.translate(this.canvasHalfW, this.canvasHalfH)
        }, t.prototype.draw = function () {
            for (var t in this.offsetX !== this.offsetTX && (this.offsetX += .02 * (this.offsetTX - this.offsetX), this.offsetY += .02 * (this.offsetTY - this.offsetY)), this.ctx.clearRect(-this.canvasHalfW, -this.canvasHalfH, this.canvasW, this.canvasH), this.stars) this.stars[t].draw(this.offsetX, this.offsetY)
        }, t.prototype.handleMouseMove = function (t) {
            this.initialized && (this.offsetTX = t.clientX - this.canvasRectLeft - this.canvasHalfW, this.offsetTY = t.clientY - this.canvasRectTop - this.canvasHalfH)
        }, t.prototype.resetMouseOffset = function () {
            this.offsetTX = 0, this.offsetTY = 0
        }, t.prototype.start = function () {
            this.engine.start()
        }, t.prototype.stop = function () {
            this.engine.stop()
        }, t.prototype.reset = function () {
            this.stars = [], this.setupCanvas(), this.generateStars()
        }, t.prototype.setMaxV = function (t) {
            this.maxV = t ? Math.abs(t) : this.defaultMaxV, this.reset()
        }, t.prototype.setMinV = function (t) {
            this.minV = t ? Math.abs(t) : this.defaultMinV, this.reset()
        }, t.prototype.setNumStars = function (t) {
            this.numStars = t ? Math.abs(t) : this.defaultNumStars, this.reset()
        }, t.prototype.setFollowMouse = function (t) {
            t ? this.followContext.addEventListener("mousemove", this.handleMouseMove) : (this.followContext.removeEventListener("mousemove", this.handleMouseMove), this.resetMouseOffset())
        }, t
    }()
}]);
//# sourceMappingURL=StarFieldCanvas.js.map