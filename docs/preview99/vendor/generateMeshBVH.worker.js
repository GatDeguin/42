var Fn=0,ki=1,Hi=2;var Gi=0,Wi=1,Xi=2,qi=3,Yi=4,Zi=5,Ji=6,$i=7;var Ki=300;var Ri=1e3,Ve=1001,Ii=1002;var zs=1006;var Vs=1008;var ks=1009;var Hs=1015;var Gs=1023;var He=2300,yn=2301,_n=2302,Pi=2400,Di=2401,Li=2402;var Qi="",gt="srgb",Ui="srgb-linear",Ni="linear",xn="srgb";var Fi=35044;var ke=2e3,Bi=2001;var ye=class{addEventListener(t,e){this._listeners===void 0&&(this._listeners={});let n=this._listeners;n[t]===void 0&&(n[t]=[]),n[t].indexOf(e)===-1&&n[t].push(e)}hasEventListener(t,e){let n=this._listeners;return n===void 0?!1:n[t]!==void 0&&n[t].indexOf(e)!==-1}removeEventListener(t,e){let n=this._listeners;if(n===void 0)return;let i=n[t];if(i!==void 0){let s=i.indexOf(e);s!==-1&&i.splice(s,1)}}dispatchEvent(t){let e=this._listeners;if(e===void 0)return;let n=e[t.type];if(n!==void 0){t.target=this;let i=n.slice(0);for(let s=0,r=i.length;s<r;s++)i[s].call(this,t);t.target=null}}},nt=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"];var Sl=Math.PI/180,Gr=180/Math.PI;function Bn(){let h=Math.random()*4294967295|0,t=Math.random()*4294967295|0,e=Math.random()*4294967295|0,n=Math.random()*4294967295|0;return(nt[h&255]+nt[h>>8&255]+nt[h>>16&255]+nt[h>>24&255]+"-"+nt[t&255]+nt[t>>8&255]+"-"+nt[t>>16&15|64]+nt[t>>24&255]+"-"+nt[e&63|128]+nt[e>>8&255]+"-"+nt[e>>16&255]+nt[e>>24&255]+nt[n&255]+nt[n>>8&255]+nt[n>>16&255]+nt[n>>24&255]).toLowerCase()}function U(h,t,e){return Math.max(t,Math.min(e,h))}function Wr(h,t){return(h%t+t)%t}function ai(h,t,e){return(1-e)*h+e*t}function Ne(h,t){switch(t.constructor){case Float32Array:return h;case Uint32Array:return h/4294967295;case Uint16Array:return h/65535;case Uint8Array:return h/255;case Int32Array:return Math.max(h/2147483647,-1);case Int16Array:return Math.max(h/32767,-1);case Int8Array:return Math.max(h/127,-1);default:throw new Error("Invalid component type.")}}function lt(h,t){switch(t.constructor){case Float32Array:return h;case Uint32Array:return Math.round(h*4294967295);case Uint16Array:return Math.round(h*65535);case Uint8Array:return Math.round(h*255);case Int32Array:return Math.round(h*2147483647);case Int16Array:return Math.round(h*32767);case Int8Array:return Math.round(h*127);default:throw new Error("Invalid component type.")}}var G=class h{constructor(t=0,e=0){h.prototype.isVector2=!0,this.x=t,this.y=e}get width(){return this.x}set width(t){this.x=t}get height(){return this.y}set height(t){this.y=t}set(t,e){return this.x=t,this.y=e,this}setScalar(t){return this.x=t,this.y=t,this}setX(t){return this.x=t,this}setY(t){return this.y=t,this}setComponent(t,e){switch(t){case 0:this.x=e;break;case 1:this.y=e;break;default:throw new Error("index is out of range: "+t)}return this}getComponent(t){switch(t){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+t)}}clone(){return new this.constructor(this.x,this.y)}copy(t){return this.x=t.x,this.y=t.y,this}add(t){return this.x+=t.x,this.y+=t.y,this}addScalar(t){return this.x+=t,this.y+=t,this}addVectors(t,e){return this.x=t.x+e.x,this.y=t.y+e.y,this}addScaledVector(t,e){return this.x+=t.x*e,this.y+=t.y*e,this}sub(t){return this.x-=t.x,this.y-=t.y,this}subScalar(t){return this.x-=t,this.y-=t,this}subVectors(t,e){return this.x=t.x-e.x,this.y=t.y-e.y,this}multiply(t){return this.x*=t.x,this.y*=t.y,this}multiplyScalar(t){return this.x*=t,this.y*=t,this}divide(t){return this.x/=t.x,this.y/=t.y,this}divideScalar(t){return this.multiplyScalar(1/t)}applyMatrix3(t){let e=this.x,n=this.y,i=t.elements;return this.x=i[0]*e+i[3]*n+i[6],this.y=i[1]*e+i[4]*n+i[7],this}min(t){return this.x=Math.min(this.x,t.x),this.y=Math.min(this.y,t.y),this}max(t){return this.x=Math.max(this.x,t.x),this.y=Math.max(this.y,t.y),this}clamp(t,e){return this.x=U(this.x,t.x,e.x),this.y=U(this.y,t.y,e.y),this}clampScalar(t,e){return this.x=U(this.x,t,e),this.y=U(this.y,t,e),this}clampLength(t,e){let n=this.length();return this.divideScalar(n||1).multiplyScalar(U(n,t,e))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(t){return this.x*t.x+this.y*t.y}cross(t){return this.x*t.y-this.y*t.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(t){let e=Math.sqrt(this.lengthSq()*t.lengthSq());if(e===0)return Math.PI/2;let n=this.dot(t)/e;return Math.acos(U(n,-1,1))}distanceTo(t){return Math.sqrt(this.distanceToSquared(t))}distanceToSquared(t){let e=this.x-t.x,n=this.y-t.y;return e*e+n*n}manhattanDistanceTo(t){return Math.abs(this.x-t.x)+Math.abs(this.y-t.y)}setLength(t){return this.normalize().multiplyScalar(t)}lerp(t,e){return this.x+=(t.x-this.x)*e,this.y+=(t.y-this.y)*e,this}lerpVectors(t,e,n){return this.x=t.x+(e.x-t.x)*n,this.y=t.y+(e.y-t.y)*n,this}equals(t){return t.x===this.x&&t.y===this.y}fromArray(t,e=0){return this.x=t[e],this.y=t[e+1],this}toArray(t=[],e=0){return t[e]=this.x,t[e+1]=this.y,t}fromBufferAttribute(t,e){return this.x=t.getX(e),this.y=t.getY(e),this}rotateAround(t,e){let n=Math.cos(e),i=Math.sin(e),s=this.x-t.x,r=this.y-t.y;return this.x=s*n-r*i+t.x,this.y=s*i+r*n+t.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}},Pt=class{constructor(t=0,e=0,n=0,i=1){this.isQuaternion=!0,this._x=t,this._y=e,this._z=n,this._w=i}static slerpFlat(t,e,n,i,s,r,o){let a=n[i+0],c=n[i+1],l=n[i+2],f=n[i+3],u=s[r+0],d=s[r+1],p=s[r+2],m=s[r+3];if(o===0){t[e+0]=a,t[e+1]=c,t[e+2]=l,t[e+3]=f;return}if(o===1){t[e+0]=u,t[e+1]=d,t[e+2]=p,t[e+3]=m;return}if(f!==m||a!==u||c!==d||l!==p){let v=1-o,y=a*u+c*d+l*p+f*m,g=y>=0?1:-1,M=1-y*y;if(M>Number.EPSILON){let _=Math.sqrt(M),E=Math.atan2(_,y*g);v=Math.sin(v*E)/_,o=Math.sin(o*E)/_}let x=o*g;if(a=a*v+u*x,c=c*v+d*x,l=l*v+p*x,f=f*v+m*x,v===1-o){let _=1/Math.sqrt(a*a+c*c+l*l+f*f);a*=_,c*=_,l*=_,f*=_}}t[e]=a,t[e+1]=c,t[e+2]=l,t[e+3]=f}static multiplyQuaternionsFlat(t,e,n,i,s,r){let o=n[i],a=n[i+1],c=n[i+2],l=n[i+3],f=s[r],u=s[r+1],d=s[r+2],p=s[r+3];return t[e]=o*p+l*f+a*d-c*u,t[e+1]=a*p+l*u+c*f-o*d,t[e+2]=c*p+l*d+o*u-a*f,t[e+3]=l*p-o*f-a*u-c*d,t}get x(){return this._x}set x(t){this._x=t,this._onChangeCallback()}get y(){return this._y}set y(t){this._y=t,this._onChangeCallback()}get z(){return this._z}set z(t){this._z=t,this._onChangeCallback()}get w(){return this._w}set w(t){this._w=t,this._onChangeCallback()}set(t,e,n,i){return this._x=t,this._y=e,this._z=n,this._w=i,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(t){return this._x=t.x,this._y=t.y,this._z=t.z,this._w=t.w,this._onChangeCallback(),this}setFromEuler(t,e=!0){let n=t._x,i=t._y,s=t._z,r=t._order,o=Math.cos,a=Math.sin,c=o(n/2),l=o(i/2),f=o(s/2),u=a(n/2),d=a(i/2),p=a(s/2);switch(r){case"XYZ":this._x=u*l*f+c*d*p,this._y=c*d*f-u*l*p,this._z=c*l*p+u*d*f,this._w=c*l*f-u*d*p;break;case"YXZ":this._x=u*l*f+c*d*p,this._y=c*d*f-u*l*p,this._z=c*l*p-u*d*f,this._w=c*l*f+u*d*p;break;case"ZXY":this._x=u*l*f-c*d*p,this._y=c*d*f+u*l*p,this._z=c*l*p+u*d*f,this._w=c*l*f-u*d*p;break;case"ZYX":this._x=u*l*f-c*d*p,this._y=c*d*f+u*l*p,this._z=c*l*p-u*d*f,this._w=c*l*f+u*d*p;break;case"YZX":this._x=u*l*f+c*d*p,this._y=c*d*f+u*l*p,this._z=c*l*p-u*d*f,this._w=c*l*f-u*d*p;break;case"XZY":this._x=u*l*f-c*d*p,this._y=c*d*f-u*l*p,this._z=c*l*p+u*d*f,this._w=c*l*f+u*d*p;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+r)}return e===!0&&this._onChangeCallback(),this}setFromAxisAngle(t,e){let n=e/2,i=Math.sin(n);return this._x=t.x*i,this._y=t.y*i,this._z=t.z*i,this._w=Math.cos(n),this._onChangeCallback(),this}setFromRotationMatrix(t){let e=t.elements,n=e[0],i=e[4],s=e[8],r=e[1],o=e[5],a=e[9],c=e[2],l=e[6],f=e[10],u=n+o+f;if(u>0){let d=.5/Math.sqrt(u+1);this._w=.25/d,this._x=(l-a)*d,this._y=(s-c)*d,this._z=(r-i)*d}else if(n>o&&n>f){let d=2*Math.sqrt(1+n-o-f);this._w=(l-a)/d,this._x=.25*d,this._y=(i+r)/d,this._z=(s+c)/d}else if(o>f){let d=2*Math.sqrt(1+o-n-f);this._w=(s-c)/d,this._x=(i+r)/d,this._y=.25*d,this._z=(a+l)/d}else{let d=2*Math.sqrt(1+f-n-o);this._w=(r-i)/d,this._x=(s+c)/d,this._y=(a+l)/d,this._z=.25*d}return this._onChangeCallback(),this}setFromUnitVectors(t,e){let n=t.dot(e)+1;return n<1e-8?(n=0,Math.abs(t.x)>Math.abs(t.z)?(this._x=-t.y,this._y=t.x,this._z=0,this._w=n):(this._x=0,this._y=-t.z,this._z=t.y,this._w=n)):(this._x=t.y*e.z-t.z*e.y,this._y=t.z*e.x-t.x*e.z,this._z=t.x*e.y-t.y*e.x,this._w=n),this.normalize()}angleTo(t){return 2*Math.acos(Math.abs(U(this.dot(t),-1,1)))}rotateTowards(t,e){let n=this.angleTo(t);if(n===0)return this;let i=Math.min(1,e/n);return this.slerp(t,i),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(t){return this._x*t._x+this._y*t._y+this._z*t._z+this._w*t._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let t=this.length();return t===0?(this._x=0,this._y=0,this._z=0,this._w=1):(t=1/t,this._x=this._x*t,this._y=this._y*t,this._z=this._z*t,this._w=this._w*t),this._onChangeCallback(),this}multiply(t){return this.multiplyQuaternions(this,t)}premultiply(t){return this.multiplyQuaternions(t,this)}multiplyQuaternions(t,e){let n=t._x,i=t._y,s=t._z,r=t._w,o=e._x,a=e._y,c=e._z,l=e._w;return this._x=n*l+r*o+i*c-s*a,this._y=i*l+r*a+s*o-n*c,this._z=s*l+r*c+n*a-i*o,this._w=r*l-n*o-i*a-s*c,this._onChangeCallback(),this}slerp(t,e){if(e===0)return this;if(e===1)return this.copy(t);let n=this._x,i=this._y,s=this._z,r=this._w,o=r*t._w+n*t._x+i*t._y+s*t._z;if(o<0?(this._w=-t._w,this._x=-t._x,this._y=-t._y,this._z=-t._z,o=-o):this.copy(t),o>=1)return this._w=r,this._x=n,this._y=i,this._z=s,this;let a=1-o*o;if(a<=Number.EPSILON){let d=1-e;return this._w=d*r+e*this._w,this._x=d*n+e*this._x,this._y=d*i+e*this._y,this._z=d*s+e*this._z,this.normalize(),this}let c=Math.sqrt(a),l=Math.atan2(c,o),f=Math.sin((1-e)*l)/c,u=Math.sin(e*l)/c;return this._w=r*f+this._w*u,this._x=n*f+this._x*u,this._y=i*f+this._y*u,this._z=s*f+this._z*u,this._onChangeCallback(),this}slerpQuaternions(t,e,n){return this.copy(t).slerp(e,n)}random(){let t=2*Math.PI*Math.random(),e=2*Math.PI*Math.random(),n=Math.random(),i=Math.sqrt(1-n),s=Math.sqrt(n);return this.set(i*Math.sin(t),i*Math.cos(t),s*Math.sin(e),s*Math.cos(e))}equals(t){return t._x===this._x&&t._y===this._y&&t._z===this._z&&t._w===this._w}fromArray(t,e=0){return this._x=t[e],this._y=t[e+1],this._z=t[e+2],this._w=t[e+3],this._onChangeCallback(),this}toArray(t=[],e=0){return t[e]=this._x,t[e+1]=this._y,t[e+2]=this._z,t[e+3]=this._w,t}fromBufferAttribute(t,e){return this._x=t.getX(e),this._y=t.getY(e),this._z=t.getZ(e),this._w=t.getW(e),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(t){return this._onChangeCallback=t,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}},S=class h{constructor(t=0,e=0,n=0){h.prototype.isVector3=!0,this.x=t,this.y=e,this.z=n}set(t,e,n){return n===void 0&&(n=this.z),this.x=t,this.y=e,this.z=n,this}setScalar(t){return this.x=t,this.y=t,this.z=t,this}setX(t){return this.x=t,this}setY(t){return this.y=t,this}setZ(t){return this.z=t,this}setComponent(t,e){switch(t){case 0:this.x=e;break;case 1:this.y=e;break;case 2:this.z=e;break;default:throw new Error("index is out of range: "+t)}return this}getComponent(t){switch(t){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+t)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(t){return this.x=t.x,this.y=t.y,this.z=t.z,this}add(t){return this.x+=t.x,this.y+=t.y,this.z+=t.z,this}addScalar(t){return this.x+=t,this.y+=t,this.z+=t,this}addVectors(t,e){return this.x=t.x+e.x,this.y=t.y+e.y,this.z=t.z+e.z,this}addScaledVector(t,e){return this.x+=t.x*e,this.y+=t.y*e,this.z+=t.z*e,this}sub(t){return this.x-=t.x,this.y-=t.y,this.z-=t.z,this}subScalar(t){return this.x-=t,this.y-=t,this.z-=t,this}subVectors(t,e){return this.x=t.x-e.x,this.y=t.y-e.y,this.z=t.z-e.z,this}multiply(t){return this.x*=t.x,this.y*=t.y,this.z*=t.z,this}multiplyScalar(t){return this.x*=t,this.y*=t,this.z*=t,this}multiplyVectors(t,e){return this.x=t.x*e.x,this.y=t.y*e.y,this.z=t.z*e.z,this}applyEuler(t){return this.applyQuaternion(As.setFromEuler(t))}applyAxisAngle(t,e){return this.applyQuaternion(As.setFromAxisAngle(t,e))}applyMatrix3(t){let e=this.x,n=this.y,i=this.z,s=t.elements;return this.x=s[0]*e+s[3]*n+s[6]*i,this.y=s[1]*e+s[4]*n+s[7]*i,this.z=s[2]*e+s[5]*n+s[8]*i,this}applyNormalMatrix(t){return this.applyMatrix3(t).normalize()}applyMatrix4(t){let e=this.x,n=this.y,i=this.z,s=t.elements,r=1/(s[3]*e+s[7]*n+s[11]*i+s[15]);return this.x=(s[0]*e+s[4]*n+s[8]*i+s[12])*r,this.y=(s[1]*e+s[5]*n+s[9]*i+s[13])*r,this.z=(s[2]*e+s[6]*n+s[10]*i+s[14])*r,this}applyQuaternion(t){let e=this.x,n=this.y,i=this.z,s=t.x,r=t.y,o=t.z,a=t.w,c=2*(r*i-o*n),l=2*(o*e-s*i),f=2*(s*n-r*e);return this.x=e+a*c+r*f-o*l,this.y=n+a*l+o*c-s*f,this.z=i+a*f+s*l-r*c,this}project(t){return this.applyMatrix4(t.matrixWorldInverse).applyMatrix4(t.projectionMatrix)}unproject(t){return this.applyMatrix4(t.projectionMatrixInverse).applyMatrix4(t.matrixWorld)}transformDirection(t){let e=this.x,n=this.y,i=this.z,s=t.elements;return this.x=s[0]*e+s[4]*n+s[8]*i,this.y=s[1]*e+s[5]*n+s[9]*i,this.z=s[2]*e+s[6]*n+s[10]*i,this.normalize()}divide(t){return this.x/=t.x,this.y/=t.y,this.z/=t.z,this}divideScalar(t){return this.multiplyScalar(1/t)}min(t){return this.x=Math.min(this.x,t.x),this.y=Math.min(this.y,t.y),this.z=Math.min(this.z,t.z),this}max(t){return this.x=Math.max(this.x,t.x),this.y=Math.max(this.y,t.y),this.z=Math.max(this.z,t.z),this}clamp(t,e){return this.x=U(this.x,t.x,e.x),this.y=U(this.y,t.y,e.y),this.z=U(this.z,t.z,e.z),this}clampScalar(t,e){return this.x=U(this.x,t,e),this.y=U(this.y,t,e),this.z=U(this.z,t,e),this}clampLength(t,e){let n=this.length();return this.divideScalar(n||1).multiplyScalar(U(n,t,e))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(t){return this.x*t.x+this.y*t.y+this.z*t.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(t){return this.normalize().multiplyScalar(t)}lerp(t,e){return this.x+=(t.x-this.x)*e,this.y+=(t.y-this.y)*e,this.z+=(t.z-this.z)*e,this}lerpVectors(t,e,n){return this.x=t.x+(e.x-t.x)*n,this.y=t.y+(e.y-t.y)*n,this.z=t.z+(e.z-t.z)*n,this}cross(t){return this.crossVectors(this,t)}crossVectors(t,e){let n=t.x,i=t.y,s=t.z,r=e.x,o=e.y,a=e.z;return this.x=i*a-s*o,this.y=s*r-n*a,this.z=n*o-i*r,this}projectOnVector(t){let e=t.lengthSq();if(e===0)return this.set(0,0,0);let n=t.dot(this)/e;return this.copy(t).multiplyScalar(n)}projectOnPlane(t){return ci.copy(this).projectOnVector(t),this.sub(ci)}reflect(t){return this.sub(ci.copy(t).multiplyScalar(2*this.dot(t)))}angleTo(t){let e=Math.sqrt(this.lengthSq()*t.lengthSq());if(e===0)return Math.PI/2;let n=this.dot(t)/e;return Math.acos(U(n,-1,1))}distanceTo(t){return Math.sqrt(this.distanceToSquared(t))}distanceToSquared(t){let e=this.x-t.x,n=this.y-t.y,i=this.z-t.z;return e*e+n*n+i*i}manhattanDistanceTo(t){return Math.abs(this.x-t.x)+Math.abs(this.y-t.y)+Math.abs(this.z-t.z)}setFromSpherical(t){return this.setFromSphericalCoords(t.radius,t.phi,t.theta)}setFromSphericalCoords(t,e,n){let i=Math.sin(e)*t;return this.x=i*Math.sin(n),this.y=Math.cos(e)*t,this.z=i*Math.cos(n),this}setFromCylindrical(t){return this.setFromCylindricalCoords(t.radius,t.theta,t.y)}setFromCylindricalCoords(t,e,n){return this.x=t*Math.sin(e),this.y=n,this.z=t*Math.cos(e),this}setFromMatrixPosition(t){let e=t.elements;return this.x=e[12],this.y=e[13],this.z=e[14],this}setFromMatrixScale(t){let e=this.setFromMatrixColumn(t,0).length(),n=this.setFromMatrixColumn(t,1).length(),i=this.setFromMatrixColumn(t,2).length();return this.x=e,this.y=n,this.z=i,this}setFromMatrixColumn(t,e){return this.fromArray(t.elements,e*4)}setFromMatrix3Column(t,e){return this.fromArray(t.elements,e*3)}setFromEuler(t){return this.x=t._x,this.y=t._y,this.z=t._z,this}setFromColor(t){return this.x=t.r,this.y=t.g,this.z=t.b,this}equals(t){return t.x===this.x&&t.y===this.y&&t.z===this.z}fromArray(t,e=0){return this.x=t[e],this.y=t[e+1],this.z=t[e+2],this}toArray(t=[],e=0){return t[e]=this.x,t[e+1]=this.y,t[e+2]=this.z,t}fromBufferAttribute(t,e){return this.x=t.getX(e),this.y=t.getY(e),this.z=t.getZ(e),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){let t=Math.random()*Math.PI*2,e=Math.random()*2-1,n=Math.sqrt(1-e*e);return this.x=n*Math.cos(t),this.y=e,this.z=n*Math.sin(t),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}},ci=new S,As=new Pt,N=class h{constructor(t,e,n,i,s,r,o,a,c){h.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],t!==void 0&&this.set(t,e,n,i,s,r,o,a,c)}set(t,e,n,i,s,r,o,a,c){let l=this.elements;return l[0]=t,l[1]=i,l[2]=o,l[3]=e,l[4]=s,l[5]=a,l[6]=n,l[7]=r,l[8]=c,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(t){let e=this.elements,n=t.elements;return e[0]=n[0],e[1]=n[1],e[2]=n[2],e[3]=n[3],e[4]=n[4],e[5]=n[5],e[6]=n[6],e[7]=n[7],e[8]=n[8],this}extractBasis(t,e,n){return t.setFromMatrix3Column(this,0),e.setFromMatrix3Column(this,1),n.setFromMatrix3Column(this,2),this}setFromMatrix4(t){let e=t.elements;return this.set(e[0],e[4],e[8],e[1],e[5],e[9],e[2],e[6],e[10]),this}multiply(t){return this.multiplyMatrices(this,t)}premultiply(t){return this.multiplyMatrices(t,this)}multiplyMatrices(t,e){let n=t.elements,i=e.elements,s=this.elements,r=n[0],o=n[3],a=n[6],c=n[1],l=n[4],f=n[7],u=n[2],d=n[5],p=n[8],m=i[0],v=i[3],y=i[6],g=i[1],M=i[4],x=i[7],_=i[2],E=i[5],b=i[8];return s[0]=r*m+o*g+a*_,s[3]=r*v+o*M+a*E,s[6]=r*y+o*x+a*b,s[1]=c*m+l*g+f*_,s[4]=c*v+l*M+f*E,s[7]=c*y+l*x+f*b,s[2]=u*m+d*g+p*_,s[5]=u*v+d*M+p*E,s[8]=u*y+d*x+p*b,this}multiplyScalar(t){let e=this.elements;return e[0]*=t,e[3]*=t,e[6]*=t,e[1]*=t,e[4]*=t,e[7]*=t,e[2]*=t,e[5]*=t,e[8]*=t,this}determinant(){let t=this.elements,e=t[0],n=t[1],i=t[2],s=t[3],r=t[4],o=t[5],a=t[6],c=t[7],l=t[8];return e*r*l-e*o*c-n*s*l+n*o*a+i*s*c-i*r*a}invert(){let t=this.elements,e=t[0],n=t[1],i=t[2],s=t[3],r=t[4],o=t[5],a=t[6],c=t[7],l=t[8],f=l*r-o*c,u=o*a-l*s,d=c*s-r*a,p=e*f+n*u+i*d;if(p===0)return this.set(0,0,0,0,0,0,0,0,0);let m=1/p;return t[0]=f*m,t[1]=(i*c-l*n)*m,t[2]=(o*n-i*r)*m,t[3]=u*m,t[4]=(l*e-i*a)*m,t[5]=(i*s-o*e)*m,t[6]=d*m,t[7]=(n*a-c*e)*m,t[8]=(r*e-n*s)*m,this}transpose(){let t,e=this.elements;return t=e[1],e[1]=e[3],e[3]=t,t=e[2],e[2]=e[6],e[6]=t,t=e[5],e[5]=e[7],e[7]=t,this}getNormalMatrix(t){return this.setFromMatrix4(t).invert().transpose()}transposeIntoArray(t){let e=this.elements;return t[0]=e[0],t[1]=e[3],t[2]=e[6],t[3]=e[1],t[4]=e[4],t[5]=e[7],t[6]=e[2],t[7]=e[5],t[8]=e[8],this}setUvTransform(t,e,n,i,s,r,o){let a=Math.cos(s),c=Math.sin(s);return this.set(n*a,n*c,-n*(a*r+c*o)+r+t,-i*c,i*a,-i*(-c*r+a*o)+o+e,0,0,1),this}scale(t,e){return this.premultiply(li.makeScale(t,e)),this}rotate(t){return this.premultiply(li.makeRotation(-t)),this}translate(t,e){return this.premultiply(li.makeTranslation(t,e)),this}makeTranslation(t,e){return t.isVector2?this.set(1,0,t.x,0,1,t.y,0,0,1):this.set(1,0,t,0,1,e,0,0,1),this}makeRotation(t){let e=Math.cos(t),n=Math.sin(t);return this.set(e,-n,0,n,e,0,0,0,1),this}makeScale(t,e){return this.set(t,0,0,0,e,0,0,0,1),this}equals(t){let e=this.elements,n=t.elements;for(let i=0;i<9;i++)if(e[i]!==n[i])return!1;return!0}fromArray(t,e=0){for(let n=0;n<9;n++)this.elements[n]=t[n+e];return this}toArray(t=[],e=0){let n=this.elements;return t[e]=n[0],t[e+1]=n[1],t[e+2]=n[2],t[e+3]=n[3],t[e+4]=n[4],t[e+5]=n[5],t[e+6]=n[6],t[e+7]=n[7],t[e+8]=n[8],t}clone(){return new this.constructor().fromArray(this.elements)}},li=new N;function Ws(h){for(let t=h.length-1;t>=0;--t)if(h[t]>=65535)return!0;return!1}function Oi(h){return document.createElementNS("http://www.w3.org/1999/xhtml",h)}var ws={};function zi(h){h in ws||(ws[h]=!0,console.warn(h))}var Cs=new N().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),Rs=new N().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function Xr(){let h={enabled:!0,workingColorSpace:Ui,spaces:{},convert:function(i,s,r){return this.enabled===!1||s===r||!s||!r||(this.spaces[s].transfer===xn&&(i.r=It(i.r),i.g=It(i.g),i.b=It(i.b)),this.spaces[s].primaries!==this.spaces[r].primaries&&(i.applyMatrix3(this.spaces[s].toXYZ),i.applyMatrix3(this.spaces[r].fromXYZ)),this.spaces[r].transfer===xn&&(i.r=xe(i.r),i.g=xe(i.g),i.b=xe(i.b))),i},workingToColorSpace:function(i,s){return this.convert(i,this.workingColorSpace,s)},colorSpaceToWorking:function(i,s){return this.convert(i,s,this.workingColorSpace)},getPrimaries:function(i){return this.spaces[i].primaries},getTransfer:function(i){return i===Qi?Ni:this.spaces[i].transfer},getToneMappingMode:function(i){return this.spaces[i].outputColorSpaceConfig.toneMappingMode||"standard"},getLuminanceCoefficients:function(i,s=this.workingColorSpace){return i.fromArray(this.spaces[s].luminanceCoefficients)},define:function(i){Object.assign(this.spaces,i)},_getMatrix:function(i,s,r){return i.copy(this.spaces[s].toXYZ).multiply(this.spaces[r].fromXYZ)},_getDrawingBufferColorSpace:function(i){return this.spaces[i].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(i=this.workingColorSpace){return this.spaces[i].workingColorSpaceConfig.unpackColorSpace},fromWorkingColorSpace:function(i,s){return zi("THREE.ColorManagement: .fromWorkingColorSpace() has been renamed to .workingToColorSpace()."),h.workingToColorSpace(i,s)},toWorkingColorSpace:function(i,s){return zi("THREE.ColorManagement: .toWorkingColorSpace() has been renamed to .colorSpaceToWorking()."),h.colorSpaceToWorking(i,s)}},t=[.64,.33,.3,.6,.15,.06],e=[.2126,.7152,.0722],n=[.3127,.329];return h.define({[Ui]:{primaries:t,whitePoint:n,transfer:Ni,toXYZ:Cs,fromXYZ:Rs,luminanceCoefficients:e,workingColorSpaceConfig:{unpackColorSpace:gt},outputColorSpaceConfig:{drawingBufferColorSpace:gt}},[gt]:{primaries:t,whitePoint:n,transfer:xn,toXYZ:Cs,fromXYZ:Rs,luminanceCoefficients:e,outputColorSpaceConfig:{drawingBufferColorSpace:gt}}}),h}var mt=Xr();function It(h){return h<.04045?h*.0773993808:Math.pow(h*.9478672986+.0521327014,2.4)}function xe(h){return h<.0031308?h*12.92:1.055*Math.pow(h,.41666)-.055}var oe,vn=class{static getDataURL(t,e="image/png"){if(/^data:/i.test(t.src)||typeof HTMLCanvasElement>"u")return t.src;let n;if(t instanceof HTMLCanvasElement)n=t;else{oe===void 0&&(oe=Oi("canvas")),oe.width=t.width,oe.height=t.height;let i=oe.getContext("2d");t instanceof ImageData?i.putImageData(t,0,0):i.drawImage(t,0,0,t.width,t.height),n=oe}return n.toDataURL(e)}static sRGBToLinear(t){if(typeof HTMLImageElement<"u"&&t instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&t instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&t instanceof ImageBitmap){let e=Oi("canvas");e.width=t.width,e.height=t.height;let n=e.getContext("2d");n.drawImage(t,0,0,t.width,t.height);let i=n.getImageData(0,0,t.width,t.height),s=i.data;for(let r=0;r<s.length;r++)s[r]=It(s[r]/255)*255;return n.putImageData(i,0,0),e}else if(t.data){let e=t.data.slice(0);for(let n=0;n<e.length;n++)e instanceof Uint8Array||e instanceof Uint8ClampedArray?e[n]=Math.floor(It(e[n]/255)*255):e[n]=It(e[n]);return{data:e,width:t.width,height:t.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),t}},qr=0,Mn=class{constructor(t=null){this.isSource=!0,Object.defineProperty(this,"id",{value:qr++}),this.uuid=Bn(),this.data=t,this.dataReady=!0,this.version=0}getSize(t){let e=this.data;return typeof HTMLVideoElement<"u"&&e instanceof HTMLVideoElement?t.set(e.videoWidth,e.videoHeight,0):e instanceof VideoFrame?t.set(e.displayHeight,e.displayWidth,0):e!==null?t.set(e.width,e.height,e.depth||0):t.set(0,0,0),t}set needsUpdate(t){t===!0&&this.version++}toJSON(t){let e=t===void 0||typeof t=="string";if(!e&&t.images[this.uuid]!==void 0)return t.images[this.uuid];let n={uuid:this.uuid,url:""},i=this.data;if(i!==null){let s;if(Array.isArray(i)){s=[];for(let r=0,o=i.length;r<o;r++)i[r].isDataTexture?s.push(ui(i[r].image)):s.push(ui(i[r]))}else s=ui(i);n.url=s}return e||(t.images[this.uuid]=n),n}};function ui(h){return typeof HTMLImageElement<"u"&&h instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&h instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&h instanceof ImageBitmap?vn.getDataURL(h):h.data?{data:Array.from(h.data),width:h.width,height:h.height,type:h.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}var Yr=0,hi=new S,ve=class h extends ye{constructor(t=h.DEFAULT_IMAGE,e=h.DEFAULT_MAPPING,n=Ve,i=Ve,s=zs,r=Vs,o=Gs,a=ks,c=h.DEFAULT_ANISOTROPY,l=Qi){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:Yr++}),this.uuid=Bn(),this.name="",this.source=new Mn(t),this.mipmaps=[],this.mapping=e,this.channel=0,this.wrapS=n,this.wrapT=i,this.magFilter=s,this.minFilter=r,this.anisotropy=c,this.format=o,this.internalFormat=null,this.type=a,this.offset=new G(0,0),this.repeat=new G(1,1),this.center=new G(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new N,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=l,this.userData={},this.updateRanges=[],this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.isArrayTexture=!!(t&&t.depth&&t.depth>1),this.pmremVersion=0}get width(){return this.source.getSize(hi).x}get height(){return this.source.getSize(hi).y}get depth(){return this.source.getSize(hi).z}get image(){return this.source.data}set image(t=null){this.source.data=t}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}addUpdateRange(t,e){this.updateRanges.push({start:t,count:e})}clearUpdateRanges(){this.updateRanges.length=0}clone(){return new this.constructor().copy(this)}copy(t){return this.name=t.name,this.source=t.source,this.mipmaps=t.mipmaps.slice(0),this.mapping=t.mapping,this.channel=t.channel,this.wrapS=t.wrapS,this.wrapT=t.wrapT,this.magFilter=t.magFilter,this.minFilter=t.minFilter,this.anisotropy=t.anisotropy,this.format=t.format,this.internalFormat=t.internalFormat,this.type=t.type,this.offset.copy(t.offset),this.repeat.copy(t.repeat),this.center.copy(t.center),this.rotation=t.rotation,this.matrixAutoUpdate=t.matrixAutoUpdate,this.matrix.copy(t.matrix),this.generateMipmaps=t.generateMipmaps,this.premultiplyAlpha=t.premultiplyAlpha,this.flipY=t.flipY,this.unpackAlignment=t.unpackAlignment,this.colorSpace=t.colorSpace,this.renderTarget=t.renderTarget,this.isRenderTargetTexture=t.isRenderTargetTexture,this.isArrayTexture=t.isArrayTexture,this.userData=JSON.parse(JSON.stringify(t.userData)),this.needsUpdate=!0,this}setValues(t){for(let e in t){let n=t[e];if(n===void 0){console.warn(`THREE.Texture.setValues(): parameter '${e}' has value of undefined.`);continue}let i=this[e];if(i===void 0){console.warn(`THREE.Texture.setValues(): property '${e}' does not exist.`);continue}i&&n&&i.isVector2&&n.isVector2||i&&n&&i.isVector3&&n.isVector3||i&&n&&i.isMatrix3&&n.isMatrix3?i.copy(n):this[e]=n}}toJSON(t){let e=t===void 0||typeof t=="string";if(!e&&t.textures[this.uuid]!==void 0)return t.textures[this.uuid];let n={metadata:{version:4.7,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(t).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(n.userData=this.userData),e||(t.textures[this.uuid]=n),n}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(t){if(this.mapping!==Ki)return t;if(t.applyMatrix3(this.matrix),t.x<0||t.x>1)switch(this.wrapS){case Ri:t.x=t.x-Math.floor(t.x);break;case Ve:t.x=t.x<0?0:1;break;case Ii:Math.abs(Math.floor(t.x)%2)===1?t.x=Math.ceil(t.x)-t.x:t.x=t.x-Math.floor(t.x);break}if(t.y<0||t.y>1)switch(this.wrapT){case Ri:t.y=t.y-Math.floor(t.y);break;case Ve:t.y=t.y<0?0:1;break;case Ii:Math.abs(Math.floor(t.y)%2)===1?t.y=Math.ceil(t.y)-t.y:t.y=t.y-Math.floor(t.y);break}return this.flipY&&(t.y=1-t.y),t}set needsUpdate(t){t===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(t){t===!0&&this.pmremVersion++}};ve.DEFAULT_IMAGE=null;ve.DEFAULT_MAPPING=Ki;ve.DEFAULT_ANISOTROPY=1;var Me=class h{constructor(t=0,e=0,n=0,i=1){h.prototype.isVector4=!0,this.x=t,this.y=e,this.z=n,this.w=i}get width(){return this.z}set width(t){this.z=t}get height(){return this.w}set height(t){this.w=t}set(t,e,n,i){return this.x=t,this.y=e,this.z=n,this.w=i,this}setScalar(t){return this.x=t,this.y=t,this.z=t,this.w=t,this}setX(t){return this.x=t,this}setY(t){return this.y=t,this}setZ(t){return this.z=t,this}setW(t){return this.w=t,this}setComponent(t,e){switch(t){case 0:this.x=e;break;case 1:this.y=e;break;case 2:this.z=e;break;case 3:this.w=e;break;default:throw new Error("index is out of range: "+t)}return this}getComponent(t){switch(t){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+t)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(t){return this.x=t.x,this.y=t.y,this.z=t.z,this.w=t.w!==void 0?t.w:1,this}add(t){return this.x+=t.x,this.y+=t.y,this.z+=t.z,this.w+=t.w,this}addScalar(t){return this.x+=t,this.y+=t,this.z+=t,this.w+=t,this}addVectors(t,e){return this.x=t.x+e.x,this.y=t.y+e.y,this.z=t.z+e.z,this.w=t.w+e.w,this}addScaledVector(t,e){return this.x+=t.x*e,this.y+=t.y*e,this.z+=t.z*e,this.w+=t.w*e,this}sub(t){return this.x-=t.x,this.y-=t.y,this.z-=t.z,this.w-=t.w,this}subScalar(t){return this.x-=t,this.y-=t,this.z-=t,this.w-=t,this}subVectors(t,e){return this.x=t.x-e.x,this.y=t.y-e.y,this.z=t.z-e.z,this.w=t.w-e.w,this}multiply(t){return this.x*=t.x,this.y*=t.y,this.z*=t.z,this.w*=t.w,this}multiplyScalar(t){return this.x*=t,this.y*=t,this.z*=t,this.w*=t,this}applyMatrix4(t){let e=this.x,n=this.y,i=this.z,s=this.w,r=t.elements;return this.x=r[0]*e+r[4]*n+r[8]*i+r[12]*s,this.y=r[1]*e+r[5]*n+r[9]*i+r[13]*s,this.z=r[2]*e+r[6]*n+r[10]*i+r[14]*s,this.w=r[3]*e+r[7]*n+r[11]*i+r[15]*s,this}divide(t){return this.x/=t.x,this.y/=t.y,this.z/=t.z,this.w/=t.w,this}divideScalar(t){return this.multiplyScalar(1/t)}setAxisAngleFromQuaternion(t){this.w=2*Math.acos(t.w);let e=Math.sqrt(1-t.w*t.w);return e<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=t.x/e,this.y=t.y/e,this.z=t.z/e),this}setAxisAngleFromRotationMatrix(t){let e,n,i,s,a=t.elements,c=a[0],l=a[4],f=a[8],u=a[1],d=a[5],p=a[9],m=a[2],v=a[6],y=a[10];if(Math.abs(l-u)<.01&&Math.abs(f-m)<.01&&Math.abs(p-v)<.01){if(Math.abs(l+u)<.1&&Math.abs(f+m)<.1&&Math.abs(p+v)<.1&&Math.abs(c+d+y-3)<.1)return this.set(1,0,0,0),this;e=Math.PI;let M=(c+1)/2,x=(d+1)/2,_=(y+1)/2,E=(l+u)/4,b=(f+m)/4,T=(p+v)/4;return M>x&&M>_?M<.01?(n=0,i=.707106781,s=.707106781):(n=Math.sqrt(M),i=E/n,s=b/n):x>_?x<.01?(n=.707106781,i=0,s=.707106781):(i=Math.sqrt(x),n=E/i,s=T/i):_<.01?(n=.707106781,i=.707106781,s=0):(s=Math.sqrt(_),n=b/s,i=T/s),this.set(n,i,s,e),this}let g=Math.sqrt((v-p)*(v-p)+(f-m)*(f-m)+(u-l)*(u-l));return Math.abs(g)<.001&&(g=1),this.x=(v-p)/g,this.y=(f-m)/g,this.z=(u-l)/g,this.w=Math.acos((c+d+y-1)/2),this}setFromMatrixPosition(t){let e=t.elements;return this.x=e[12],this.y=e[13],this.z=e[14],this.w=e[15],this}min(t){return this.x=Math.min(this.x,t.x),this.y=Math.min(this.y,t.y),this.z=Math.min(this.z,t.z),this.w=Math.min(this.w,t.w),this}max(t){return this.x=Math.max(this.x,t.x),this.y=Math.max(this.y,t.y),this.z=Math.max(this.z,t.z),this.w=Math.max(this.w,t.w),this}clamp(t,e){return this.x=U(this.x,t.x,e.x),this.y=U(this.y,t.y,e.y),this.z=U(this.z,t.z,e.z),this.w=U(this.w,t.w,e.w),this}clampScalar(t,e){return this.x=U(this.x,t,e),this.y=U(this.y,t,e),this.z=U(this.z,t,e),this.w=U(this.w,t,e),this}clampLength(t,e){let n=this.length();return this.divideScalar(n||1).multiplyScalar(U(n,t,e))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(t){return this.x*t.x+this.y*t.y+this.z*t.z+this.w*t.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(t){return this.normalize().multiplyScalar(t)}lerp(t,e){return this.x+=(t.x-this.x)*e,this.y+=(t.y-this.y)*e,this.z+=(t.z-this.z)*e,this.w+=(t.w-this.w)*e,this}lerpVectors(t,e,n){return this.x=t.x+(e.x-t.x)*n,this.y=t.y+(e.y-t.y)*n,this.z=t.z+(e.z-t.z)*n,this.w=t.w+(e.w-t.w)*n,this}equals(t){return t.x===this.x&&t.y===this.y&&t.z===this.z&&t.w===this.w}fromArray(t,e=0){return this.x=t[e],this.y=t[e+1],this.z=t[e+2],this.w=t[e+3],this}toArray(t=[],e=0){return t[e]=this.x,t[e+1]=this.y,t[e+2]=this.z,t[e+3]=this.w,t}fromBufferAttribute(t,e){return this.x=t.getX(e),this.y=t.getY(e),this.z=t.getZ(e),this.w=t.getW(e),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}};var Y=class{constructor(t=new S(1/0,1/0,1/0),e=new S(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=t,this.max=e}set(t,e){return this.min.copy(t),this.max.copy(e),this}setFromArray(t){this.makeEmpty();for(let e=0,n=t.length;e<n;e+=3)this.expandByPoint(yt.fromArray(t,e));return this}setFromBufferAttribute(t){this.makeEmpty();for(let e=0,n=t.count;e<n;e++)this.expandByPoint(yt.fromBufferAttribute(t,e));return this}setFromPoints(t){this.makeEmpty();for(let e=0,n=t.length;e<n;e++)this.expandByPoint(t[e]);return this}setFromCenterAndSize(t,e){let n=yt.copy(e).multiplyScalar(.5);return this.min.copy(t).sub(n),this.max.copy(t).add(n),this}setFromObject(t,e=!1){return this.makeEmpty(),this.expandByObject(t,e)}clone(){return new this.constructor().copy(this)}copy(t){return this.min.copy(t.min),this.max.copy(t.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(t){return this.isEmpty()?t.set(0,0,0):t.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(t){return this.isEmpty()?t.set(0,0,0):t.subVectors(this.max,this.min)}expandByPoint(t){return this.min.min(t),this.max.max(t),this}expandByVector(t){return this.min.sub(t),this.max.add(t),this}expandByScalar(t){return this.min.addScalar(-t),this.max.addScalar(t),this}expandByObject(t,e=!1){t.updateWorldMatrix(!1,!1);let n=t.geometry;if(n!==void 0){let s=n.getAttribute("position");if(e===!0&&s!==void 0&&t.isInstancedMesh!==!0)for(let r=0,o=s.count;r<o;r++)t.isMesh===!0?t.getVertexPosition(r,yt):yt.fromBufferAttribute(s,r),yt.applyMatrix4(t.matrixWorld),this.expandByPoint(yt);else t.boundingBox!==void 0?(t.boundingBox===null&&t.computeBoundingBox(),on.copy(t.boundingBox)):(n.boundingBox===null&&n.computeBoundingBox(),on.copy(n.boundingBox)),on.applyMatrix4(t.matrixWorld),this.union(on)}let i=t.children;for(let s=0,r=i.length;s<r;s++)this.expandByObject(i[s],e);return this}containsPoint(t){return t.x>=this.min.x&&t.x<=this.max.x&&t.y>=this.min.y&&t.y<=this.max.y&&t.z>=this.min.z&&t.z<=this.max.z}containsBox(t){return this.min.x<=t.min.x&&t.max.x<=this.max.x&&this.min.y<=t.min.y&&t.max.y<=this.max.y&&this.min.z<=t.min.z&&t.max.z<=this.max.z}getParameter(t,e){return e.set((t.x-this.min.x)/(this.max.x-this.min.x),(t.y-this.min.y)/(this.max.y-this.min.y),(t.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(t){return t.max.x>=this.min.x&&t.min.x<=this.max.x&&t.max.y>=this.min.y&&t.min.y<=this.max.y&&t.max.z>=this.min.z&&t.min.z<=this.max.z}intersectsSphere(t){return this.clampPoint(t.center,yt),yt.distanceToSquared(t.center)<=t.radius*t.radius}intersectsPlane(t){let e,n;return t.normal.x>0?(e=t.normal.x*this.min.x,n=t.normal.x*this.max.x):(e=t.normal.x*this.max.x,n=t.normal.x*this.min.x),t.normal.y>0?(e+=t.normal.y*this.min.y,n+=t.normal.y*this.max.y):(e+=t.normal.y*this.max.y,n+=t.normal.y*this.min.y),t.normal.z>0?(e+=t.normal.z*this.min.z,n+=t.normal.z*this.max.z):(e+=t.normal.z*this.max.z,n+=t.normal.z*this.min.z),e<=-t.constant&&n>=-t.constant}intersectsTriangle(t){if(this.isEmpty())return!1;this.getCenter(Fe),an.subVectors(this.max,Fe),ae.subVectors(t.a,Fe),ce.subVectors(t.b,Fe),le.subVectors(t.c,Fe),Ft.subVectors(ce,ae),Bt.subVectors(le,ce),$t.subVectors(ae,le);let e=[0,-Ft.z,Ft.y,0,-Bt.z,Bt.y,0,-$t.z,$t.y,Ft.z,0,-Ft.x,Bt.z,0,-Bt.x,$t.z,0,-$t.x,-Ft.y,Ft.x,0,-Bt.y,Bt.x,0,-$t.y,$t.x,0];return!fi(e,ae,ce,le,an)||(e=[1,0,0,0,1,0,0,0,1],!fi(e,ae,ce,le,an))?!1:(cn.crossVectors(Ft,Bt),e=[cn.x,cn.y,cn.z],fi(e,ae,ce,le,an))}clampPoint(t,e){return e.copy(t).clamp(this.min,this.max)}distanceToPoint(t){return this.clampPoint(t,yt).distanceTo(t)}getBoundingSphere(t){return this.isEmpty()?t.makeEmpty():(this.getCenter(t.center),t.radius=this.getSize(yt).length()*.5),t}intersect(t){return this.min.max(t.min),this.max.min(t.max),this.isEmpty()&&this.makeEmpty(),this}union(t){return this.min.min(t.min),this.max.max(t.max),this}applyMatrix4(t){return this.isEmpty()?this:(Et[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(t),Et[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(t),Et[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(t),Et[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(t),Et[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(t),Et[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(t),Et[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(t),Et[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(t),this.setFromPoints(Et),this)}translate(t){return this.min.add(t),this.max.add(t),this}equals(t){return t.min.equals(this.min)&&t.max.equals(this.max)}toJSON(){return{min:this.min.toArray(),max:this.max.toArray()}}fromJSON(t){return this.min.fromArray(t.min),this.max.fromArray(t.max),this}},Et=[new S,new S,new S,new S,new S,new S,new S,new S],yt=new S,on=new Y,ae=new S,ce=new S,le=new S,Ft=new S,Bt=new S,$t=new S,Fe=new S,an=new S,cn=new S,Kt=new S;function fi(h,t,e,n,i){for(let s=0,r=h.length-3;s<=r;s+=3){Kt.fromArray(h,s);let o=i.x*Math.abs(Kt.x)+i.y*Math.abs(Kt.y)+i.z*Math.abs(Kt.z),a=t.dot(Kt),c=e.dot(Kt),l=n.dot(Kt);if(Math.max(-Math.max(a,c,l),Math.min(a,c,l))>o)return!1}return!0}var Zr=new Y,Be=new S,di=new S,Sn=class{constructor(t=new S,e=-1){this.isSphere=!0,this.center=t,this.radius=e}set(t,e){return this.center.copy(t),this.radius=e,this}setFromPoints(t,e){let n=this.center;e!==void 0?n.copy(e):Zr.setFromPoints(t).getCenter(n);let i=0;for(let s=0,r=t.length;s<r;s++)i=Math.max(i,n.distanceToSquared(t[s]));return this.radius=Math.sqrt(i),this}copy(t){return this.center.copy(t.center),this.radius=t.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(t){return t.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(t){return t.distanceTo(this.center)-this.radius}intersectsSphere(t){let e=this.radius+t.radius;return t.center.distanceToSquared(this.center)<=e*e}intersectsBox(t){return t.intersectsSphere(this)}intersectsPlane(t){return Math.abs(t.distanceToPoint(this.center))<=this.radius}clampPoint(t,e){let n=this.center.distanceToSquared(t);return e.copy(t),n>this.radius*this.radius&&(e.sub(this.center).normalize(),e.multiplyScalar(this.radius).add(this.center)),e}getBoundingBox(t){return this.isEmpty()?(t.makeEmpty(),t):(t.set(this.center,this.center),t.expandByScalar(this.radius),t)}applyMatrix4(t){return this.center.applyMatrix4(t),this.radius=this.radius*t.getMaxScaleOnAxis(),this}translate(t){return this.center.add(t),this}expandByPoint(t){if(this.isEmpty())return this.center.copy(t),this.radius=0,this;Be.subVectors(t,this.center);let e=Be.lengthSq();if(e>this.radius*this.radius){let n=Math.sqrt(e),i=(n-this.radius)*.5;this.center.addScaledVector(Be,i/n),this.radius+=i}return this}union(t){return t.isEmpty()?this:this.isEmpty()?(this.copy(t),this):(this.center.equals(t.center)===!0?this.radius=Math.max(this.radius,t.radius):(di.subVectors(t.center,this.center).setLength(t.radius),this.expandByPoint(Be.copy(t.center).add(di)),this.expandByPoint(Be.copy(t.center).sub(di))),this)}equals(t){return t.center.equals(this.center)&&t.radius===this.radius}clone(){return new this.constructor().copy(this)}toJSON(){return{radius:this.radius,center:this.center.toArray()}}fromJSON(t){return this.radius=t.radius,this.center.fromArray(t.center),this}},At=new S,pi=new S,ln=new S,Ot=new S,mi=new S,un=new S,gi=new S,Ge=class{constructor(t=new S,e=new S(0,0,-1)){this.origin=t,this.direction=e}set(t,e){return this.origin.copy(t),this.direction.copy(e),this}copy(t){return this.origin.copy(t.origin),this.direction.copy(t.direction),this}at(t,e){return e.copy(this.origin).addScaledVector(this.direction,t)}lookAt(t){return this.direction.copy(t).sub(this.origin).normalize(),this}recast(t){return this.origin.copy(this.at(t,At)),this}closestPointToPoint(t,e){e.subVectors(t,this.origin);let n=e.dot(this.direction);return n<0?e.copy(this.origin):e.copy(this.origin).addScaledVector(this.direction,n)}distanceToPoint(t){return Math.sqrt(this.distanceSqToPoint(t))}distanceSqToPoint(t){let e=At.subVectors(t,this.origin).dot(this.direction);return e<0?this.origin.distanceToSquared(t):(At.copy(this.origin).addScaledVector(this.direction,e),At.distanceToSquared(t))}distanceSqToSegment(t,e,n,i){pi.copy(t).add(e).multiplyScalar(.5),ln.copy(e).sub(t).normalize(),Ot.copy(this.origin).sub(pi);let s=t.distanceTo(e)*.5,r=-this.direction.dot(ln),o=Ot.dot(this.direction),a=-Ot.dot(ln),c=Ot.lengthSq(),l=Math.abs(1-r*r),f,u,d,p;if(l>0)if(f=r*a-o,u=r*o-a,p=s*l,f>=0)if(u>=-p)if(u<=p){let m=1/l;f*=m,u*=m,d=f*(f+r*u+2*o)+u*(r*f+u+2*a)+c}else u=s,f=Math.max(0,-(r*u+o)),d=-f*f+u*(u+2*a)+c;else u=-s,f=Math.max(0,-(r*u+o)),d=-f*f+u*(u+2*a)+c;else u<=-p?(f=Math.max(0,-(-r*s+o)),u=f>0?-s:Math.min(Math.max(-s,-a),s),d=-f*f+u*(u+2*a)+c):u<=p?(f=0,u=Math.min(Math.max(-s,-a),s),d=u*(u+2*a)+c):(f=Math.max(0,-(r*s+o)),u=f>0?s:Math.min(Math.max(-s,-a),s),d=-f*f+u*(u+2*a)+c);else u=r>0?-s:s,f=Math.max(0,-(r*u+o)),d=-f*f+u*(u+2*a)+c;return n&&n.copy(this.origin).addScaledVector(this.direction,f),i&&i.copy(pi).addScaledVector(ln,u),d}intersectSphere(t,e){At.subVectors(t.center,this.origin);let n=At.dot(this.direction),i=At.dot(At)-n*n,s=t.radius*t.radius;if(i>s)return null;let r=Math.sqrt(s-i),o=n-r,a=n+r;return a<0?null:o<0?this.at(a,e):this.at(o,e)}intersectsSphere(t){return t.radius<0?!1:this.distanceSqToPoint(t.center)<=t.radius*t.radius}distanceToPlane(t){let e=t.normal.dot(this.direction);if(e===0)return t.distanceToPoint(this.origin)===0?0:null;let n=-(this.origin.dot(t.normal)+t.constant)/e;return n>=0?n:null}intersectPlane(t,e){let n=this.distanceToPlane(t);return n===null?null:this.at(n,e)}intersectsPlane(t){let e=t.distanceToPoint(this.origin);return e===0||t.normal.dot(this.direction)*e<0}intersectBox(t,e){let n,i,s,r,o,a,c=1/this.direction.x,l=1/this.direction.y,f=1/this.direction.z,u=this.origin;return c>=0?(n=(t.min.x-u.x)*c,i=(t.max.x-u.x)*c):(n=(t.max.x-u.x)*c,i=(t.min.x-u.x)*c),l>=0?(s=(t.min.y-u.y)*l,r=(t.max.y-u.y)*l):(s=(t.max.y-u.y)*l,r=(t.min.y-u.y)*l),n>r||s>i||((s>n||isNaN(n))&&(n=s),(r<i||isNaN(i))&&(i=r),f>=0?(o=(t.min.z-u.z)*f,a=(t.max.z-u.z)*f):(o=(t.max.z-u.z)*f,a=(t.min.z-u.z)*f),n>a||o>i)||((o>n||n!==n)&&(n=o),(a<i||i!==i)&&(i=a),i<0)?null:this.at(n>=0?n:i,e)}intersectsBox(t){return this.intersectBox(t,At)!==null}intersectTriangle(t,e,n,i,s){mi.subVectors(e,t),un.subVectors(n,t),gi.crossVectors(mi,un);let r=this.direction.dot(gi),o;if(r>0){if(i)return null;o=1}else if(r<0)o=-1,r=-r;else return null;Ot.subVectors(this.origin,t);let a=o*this.direction.dot(un.crossVectors(Ot,un));if(a<0)return null;let c=o*this.direction.dot(mi.cross(Ot));if(c<0||a+c>r)return null;let l=-o*Ot.dot(gi);return l<0?null:this.at(l/r,s)}applyMatrix4(t){return this.origin.applyMatrix4(t),this.direction.transformDirection(t),this}equals(t){return t.origin.equals(this.origin)&&t.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}},q=class h{constructor(t,e,n,i,s,r,o,a,c,l,f,u,d,p,m,v){h.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],t!==void 0&&this.set(t,e,n,i,s,r,o,a,c,l,f,u,d,p,m,v)}set(t,e,n,i,s,r,o,a,c,l,f,u,d,p,m,v){let y=this.elements;return y[0]=t,y[4]=e,y[8]=n,y[12]=i,y[1]=s,y[5]=r,y[9]=o,y[13]=a,y[2]=c,y[6]=l,y[10]=f,y[14]=u,y[3]=d,y[7]=p,y[11]=m,y[15]=v,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new h().fromArray(this.elements)}copy(t){let e=this.elements,n=t.elements;return e[0]=n[0],e[1]=n[1],e[2]=n[2],e[3]=n[3],e[4]=n[4],e[5]=n[5],e[6]=n[6],e[7]=n[7],e[8]=n[8],e[9]=n[9],e[10]=n[10],e[11]=n[11],e[12]=n[12],e[13]=n[13],e[14]=n[14],e[15]=n[15],this}copyPosition(t){let e=this.elements,n=t.elements;return e[12]=n[12],e[13]=n[13],e[14]=n[14],this}setFromMatrix3(t){let e=t.elements;return this.set(e[0],e[3],e[6],0,e[1],e[4],e[7],0,e[2],e[5],e[8],0,0,0,0,1),this}extractBasis(t,e,n){return t.setFromMatrixColumn(this,0),e.setFromMatrixColumn(this,1),n.setFromMatrixColumn(this,2),this}makeBasis(t,e,n){return this.set(t.x,e.x,n.x,0,t.y,e.y,n.y,0,t.z,e.z,n.z,0,0,0,0,1),this}extractRotation(t){let e=this.elements,n=t.elements,i=1/ue.setFromMatrixColumn(t,0).length(),s=1/ue.setFromMatrixColumn(t,1).length(),r=1/ue.setFromMatrixColumn(t,2).length();return e[0]=n[0]*i,e[1]=n[1]*i,e[2]=n[2]*i,e[3]=0,e[4]=n[4]*s,e[5]=n[5]*s,e[6]=n[6]*s,e[7]=0,e[8]=n[8]*r,e[9]=n[9]*r,e[10]=n[10]*r,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,this}makeRotationFromEuler(t){let e=this.elements,n=t.x,i=t.y,s=t.z,r=Math.cos(n),o=Math.sin(n),a=Math.cos(i),c=Math.sin(i),l=Math.cos(s),f=Math.sin(s);if(t.order==="XYZ"){let u=r*l,d=r*f,p=o*l,m=o*f;e[0]=a*l,e[4]=-a*f,e[8]=c,e[1]=d+p*c,e[5]=u-m*c,e[9]=-o*a,e[2]=m-u*c,e[6]=p+d*c,e[10]=r*a}else if(t.order==="YXZ"){let u=a*l,d=a*f,p=c*l,m=c*f;e[0]=u+m*o,e[4]=p*o-d,e[8]=r*c,e[1]=r*f,e[5]=r*l,e[9]=-o,e[2]=d*o-p,e[6]=m+u*o,e[10]=r*a}else if(t.order==="ZXY"){let u=a*l,d=a*f,p=c*l,m=c*f;e[0]=u-m*o,e[4]=-r*f,e[8]=p+d*o,e[1]=d+p*o,e[5]=r*l,e[9]=m-u*o,e[2]=-r*c,e[6]=o,e[10]=r*a}else if(t.order==="ZYX"){let u=r*l,d=r*f,p=o*l,m=o*f;e[0]=a*l,e[4]=p*c-d,e[8]=u*c+m,e[1]=a*f,e[5]=m*c+u,e[9]=d*c-p,e[2]=-c,e[6]=o*a,e[10]=r*a}else if(t.order==="YZX"){let u=r*a,d=r*c,p=o*a,m=o*c;e[0]=a*l,e[4]=m-u*f,e[8]=p*f+d,e[1]=f,e[5]=r*l,e[9]=-o*l,e[2]=-c*l,e[6]=d*f+p,e[10]=u-m*f}else if(t.order==="XZY"){let u=r*a,d=r*c,p=o*a,m=o*c;e[0]=a*l,e[4]=-f,e[8]=c*l,e[1]=u*f+m,e[5]=r*l,e[9]=d*f-p,e[2]=p*f-d,e[6]=o*l,e[10]=m*f+u}return e[3]=0,e[7]=0,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,this}makeRotationFromQuaternion(t){return this.compose(Jr,t,$r)}lookAt(t,e,n){let i=this.elements;return ut.subVectors(t,e),ut.lengthSq()===0&&(ut.z=1),ut.normalize(),zt.crossVectors(n,ut),zt.lengthSq()===0&&(Math.abs(n.z)===1?ut.x+=1e-4:ut.z+=1e-4,ut.normalize(),zt.crossVectors(n,ut)),zt.normalize(),hn.crossVectors(ut,zt),i[0]=zt.x,i[4]=hn.x,i[8]=ut.x,i[1]=zt.y,i[5]=hn.y,i[9]=ut.y,i[2]=zt.z,i[6]=hn.z,i[10]=ut.z,this}multiply(t){return this.multiplyMatrices(this,t)}premultiply(t){return this.multiplyMatrices(t,this)}multiplyMatrices(t,e){let n=t.elements,i=e.elements,s=this.elements,r=n[0],o=n[4],a=n[8],c=n[12],l=n[1],f=n[5],u=n[9],d=n[13],p=n[2],m=n[6],v=n[10],y=n[14],g=n[3],M=n[7],x=n[11],_=n[15],E=i[0],b=i[4],T=i[8],C=i[12],A=i[1],R=i[5],w=i[9],I=i[13],D=i[2],L=i[6],W=i[10],Tt=i[14],Zt=i[3],Jt=i[7],Ut=i[11],Nt=i[15];return s[0]=r*E+o*A+a*D+c*Zt,s[4]=r*b+o*R+a*L+c*Jt,s[8]=r*T+o*w+a*W+c*Ut,s[12]=r*C+o*I+a*Tt+c*Nt,s[1]=l*E+f*A+u*D+d*Zt,s[5]=l*b+f*R+u*L+d*Jt,s[9]=l*T+f*w+u*W+d*Ut,s[13]=l*C+f*I+u*Tt+d*Nt,s[2]=p*E+m*A+v*D+y*Zt,s[6]=p*b+m*R+v*L+y*Jt,s[10]=p*T+m*w+v*W+y*Ut,s[14]=p*C+m*I+v*Tt+y*Nt,s[3]=g*E+M*A+x*D+_*Zt,s[7]=g*b+M*R+x*L+_*Jt,s[11]=g*T+M*w+x*W+_*Ut,s[15]=g*C+M*I+x*Tt+_*Nt,this}multiplyScalar(t){let e=this.elements;return e[0]*=t,e[4]*=t,e[8]*=t,e[12]*=t,e[1]*=t,e[5]*=t,e[9]*=t,e[13]*=t,e[2]*=t,e[6]*=t,e[10]*=t,e[14]*=t,e[3]*=t,e[7]*=t,e[11]*=t,e[15]*=t,this}determinant(){let t=this.elements,e=t[0],n=t[4],i=t[8],s=t[12],r=t[1],o=t[5],a=t[9],c=t[13],l=t[2],f=t[6],u=t[10],d=t[14],p=t[3],m=t[7],v=t[11],y=t[15];return p*(+s*a*f-i*c*f-s*o*u+n*c*u+i*o*d-n*a*d)+m*(+e*a*d-e*c*u+s*r*u-i*r*d+i*c*l-s*a*l)+v*(+e*c*f-e*o*d-s*r*f+n*r*d+s*o*l-n*c*l)+y*(-i*o*l-e*a*f+e*o*u+i*r*f-n*r*u+n*a*l)}transpose(){let t=this.elements,e;return e=t[1],t[1]=t[4],t[4]=e,e=t[2],t[2]=t[8],t[8]=e,e=t[6],t[6]=t[9],t[9]=e,e=t[3],t[3]=t[12],t[12]=e,e=t[7],t[7]=t[13],t[13]=e,e=t[11],t[11]=t[14],t[14]=e,this}setPosition(t,e,n){let i=this.elements;return t.isVector3?(i[12]=t.x,i[13]=t.y,i[14]=t.z):(i[12]=t,i[13]=e,i[14]=n),this}invert(){let t=this.elements,e=t[0],n=t[1],i=t[2],s=t[3],r=t[4],o=t[5],a=t[6],c=t[7],l=t[8],f=t[9],u=t[10],d=t[11],p=t[12],m=t[13],v=t[14],y=t[15],g=f*v*c-m*u*c+m*a*d-o*v*d-f*a*y+o*u*y,M=p*u*c-l*v*c-p*a*d+r*v*d+l*a*y-r*u*y,x=l*m*c-p*f*c+p*o*d-r*m*d-l*o*y+r*f*y,_=p*f*a-l*m*a-p*o*u+r*m*u+l*o*v-r*f*v,E=e*g+n*M+i*x+s*_;if(E===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);let b=1/E;return t[0]=g*b,t[1]=(m*u*s-f*v*s-m*i*d+n*v*d+f*i*y-n*u*y)*b,t[2]=(o*v*s-m*a*s+m*i*c-n*v*c-o*i*y+n*a*y)*b,t[3]=(f*a*s-o*u*s-f*i*c+n*u*c+o*i*d-n*a*d)*b,t[4]=M*b,t[5]=(l*v*s-p*u*s+p*i*d-e*v*d-l*i*y+e*u*y)*b,t[6]=(p*a*s-r*v*s-p*i*c+e*v*c+r*i*y-e*a*y)*b,t[7]=(r*u*s-l*a*s+l*i*c-e*u*c-r*i*d+e*a*d)*b,t[8]=x*b,t[9]=(p*f*s-l*m*s-p*n*d+e*m*d+l*n*y-e*f*y)*b,t[10]=(r*m*s-p*o*s+p*n*c-e*m*c-r*n*y+e*o*y)*b,t[11]=(l*o*s-r*f*s-l*n*c+e*f*c+r*n*d-e*o*d)*b,t[12]=_*b,t[13]=(l*m*i-p*f*i+p*n*u-e*m*u-l*n*v+e*f*v)*b,t[14]=(p*o*i-r*m*i-p*n*a+e*m*a+r*n*v-e*o*v)*b,t[15]=(r*f*i-l*o*i+l*n*a-e*f*a-r*n*u+e*o*u)*b,this}scale(t){let e=this.elements,n=t.x,i=t.y,s=t.z;return e[0]*=n,e[4]*=i,e[8]*=s,e[1]*=n,e[5]*=i,e[9]*=s,e[2]*=n,e[6]*=i,e[10]*=s,e[3]*=n,e[7]*=i,e[11]*=s,this}getMaxScaleOnAxis(){let t=this.elements,e=t[0]*t[0]+t[1]*t[1]+t[2]*t[2],n=t[4]*t[4]+t[5]*t[5]+t[6]*t[6],i=t[8]*t[8]+t[9]*t[9]+t[10]*t[10];return Math.sqrt(Math.max(e,n,i))}makeTranslation(t,e,n){return t.isVector3?this.set(1,0,0,t.x,0,1,0,t.y,0,0,1,t.z,0,0,0,1):this.set(1,0,0,t,0,1,0,e,0,0,1,n,0,0,0,1),this}makeRotationX(t){let e=Math.cos(t),n=Math.sin(t);return this.set(1,0,0,0,0,e,-n,0,0,n,e,0,0,0,0,1),this}makeRotationY(t){let e=Math.cos(t),n=Math.sin(t);return this.set(e,0,n,0,0,1,0,0,-n,0,e,0,0,0,0,1),this}makeRotationZ(t){let e=Math.cos(t),n=Math.sin(t);return this.set(e,-n,0,0,n,e,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(t,e){let n=Math.cos(e),i=Math.sin(e),s=1-n,r=t.x,o=t.y,a=t.z,c=s*r,l=s*o;return this.set(c*r+n,c*o-i*a,c*a+i*o,0,c*o+i*a,l*o+n,l*a-i*r,0,c*a-i*o,l*a+i*r,s*a*a+n,0,0,0,0,1),this}makeScale(t,e,n){return this.set(t,0,0,0,0,e,0,0,0,0,n,0,0,0,0,1),this}makeShear(t,e,n,i,s,r){return this.set(1,n,s,0,t,1,r,0,e,i,1,0,0,0,0,1),this}compose(t,e,n){let i=this.elements,s=e._x,r=e._y,o=e._z,a=e._w,c=s+s,l=r+r,f=o+o,u=s*c,d=s*l,p=s*f,m=r*l,v=r*f,y=o*f,g=a*c,M=a*l,x=a*f,_=n.x,E=n.y,b=n.z;return i[0]=(1-(m+y))*_,i[1]=(d+x)*_,i[2]=(p-M)*_,i[3]=0,i[4]=(d-x)*E,i[5]=(1-(u+y))*E,i[6]=(v+g)*E,i[7]=0,i[8]=(p+M)*b,i[9]=(v-g)*b,i[10]=(1-(u+m))*b,i[11]=0,i[12]=t.x,i[13]=t.y,i[14]=t.z,i[15]=1,this}decompose(t,e,n){let i=this.elements,s=ue.set(i[0],i[1],i[2]).length(),r=ue.set(i[4],i[5],i[6]).length(),o=ue.set(i[8],i[9],i[10]).length();this.determinant()<0&&(s=-s),t.x=i[12],t.y=i[13],t.z=i[14],vt.copy(this);let c=1/s,l=1/r,f=1/o;return vt.elements[0]*=c,vt.elements[1]*=c,vt.elements[2]*=c,vt.elements[4]*=l,vt.elements[5]*=l,vt.elements[6]*=l,vt.elements[8]*=f,vt.elements[9]*=f,vt.elements[10]*=f,e.setFromRotationMatrix(vt),n.x=s,n.y=r,n.z=o,this}makePerspective(t,e,n,i,s,r,o=ke,a=!1){let c=this.elements,l=2*s/(e-t),f=2*s/(n-i),u=(e+t)/(e-t),d=(n+i)/(n-i),p,m;if(a)p=s/(r-s),m=r*s/(r-s);else if(o===ke)p=-(r+s)/(r-s),m=-2*r*s/(r-s);else if(o===Bi)p=-r/(r-s),m=-r*s/(r-s);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+o);return c[0]=l,c[4]=0,c[8]=u,c[12]=0,c[1]=0,c[5]=f,c[9]=d,c[13]=0,c[2]=0,c[6]=0,c[10]=p,c[14]=m,c[3]=0,c[7]=0,c[11]=-1,c[15]=0,this}makeOrthographic(t,e,n,i,s,r,o=ke,a=!1){let c=this.elements,l=2/(e-t),f=2/(n-i),u=-(e+t)/(e-t),d=-(n+i)/(n-i),p,m;if(a)p=1/(r-s),m=r/(r-s);else if(o===ke)p=-2/(r-s),m=-(r+s)/(r-s);else if(o===Bi)p=-1/(r-s),m=-s/(r-s);else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+o);return c[0]=l,c[4]=0,c[8]=0,c[12]=u,c[1]=0,c[5]=f,c[9]=0,c[13]=d,c[2]=0,c[6]=0,c[10]=p,c[14]=m,c[3]=0,c[7]=0,c[11]=0,c[15]=1,this}equals(t){let e=this.elements,n=t.elements;for(let i=0;i<16;i++)if(e[i]!==n[i])return!1;return!0}fromArray(t,e=0){for(let n=0;n<16;n++)this.elements[n]=t[n+e];return this}toArray(t=[],e=0){let n=this.elements;return t[e]=n[0],t[e+1]=n[1],t[e+2]=n[2],t[e+3]=n[3],t[e+4]=n[4],t[e+5]=n[5],t[e+6]=n[6],t[e+7]=n[7],t[e+8]=n[8],t[e+9]=n[9],t[e+10]=n[10],t[e+11]=n[11],t[e+12]=n[12],t[e+13]=n[13],t[e+14]=n[14],t[e+15]=n[15],t}},ue=new S,vt=new q,Jr=new S(0,0,0),$r=new S(1,1,1),zt=new S,hn=new S,ut=new S,Is=new q,Ps=new Pt,We=class h{constructor(t=0,e=0,n=0,i=h.DEFAULT_ORDER){this.isEuler=!0,this._x=t,this._y=e,this._z=n,this._order=i}get x(){return this._x}set x(t){this._x=t,this._onChangeCallback()}get y(){return this._y}set y(t){this._y=t,this._onChangeCallback()}get z(){return this._z}set z(t){this._z=t,this._onChangeCallback()}get order(){return this._order}set order(t){this._order=t,this._onChangeCallback()}set(t,e,n,i=this._order){return this._x=t,this._y=e,this._z=n,this._order=i,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(t){return this._x=t._x,this._y=t._y,this._z=t._z,this._order=t._order,this._onChangeCallback(),this}setFromRotationMatrix(t,e=this._order,n=!0){let i=t.elements,s=i[0],r=i[4],o=i[8],a=i[1],c=i[5],l=i[9],f=i[2],u=i[6],d=i[10];switch(e){case"XYZ":this._y=Math.asin(U(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(-l,d),this._z=Math.atan2(-r,s)):(this._x=Math.atan2(u,c),this._z=0);break;case"YXZ":this._x=Math.asin(-U(l,-1,1)),Math.abs(l)<.9999999?(this._y=Math.atan2(o,d),this._z=Math.atan2(a,c)):(this._y=Math.atan2(-f,s),this._z=0);break;case"ZXY":this._x=Math.asin(U(u,-1,1)),Math.abs(u)<.9999999?(this._y=Math.atan2(-f,d),this._z=Math.atan2(-r,c)):(this._y=0,this._z=Math.atan2(a,s));break;case"ZYX":this._y=Math.asin(-U(f,-1,1)),Math.abs(f)<.9999999?(this._x=Math.atan2(u,d),this._z=Math.atan2(a,s)):(this._x=0,this._z=Math.atan2(-r,c));break;case"YZX":this._z=Math.asin(U(a,-1,1)),Math.abs(a)<.9999999?(this._x=Math.atan2(-l,c),this._y=Math.atan2(-f,s)):(this._x=0,this._y=Math.atan2(o,d));break;case"XZY":this._z=Math.asin(-U(r,-1,1)),Math.abs(r)<.9999999?(this._x=Math.atan2(u,c),this._y=Math.atan2(o,s)):(this._x=Math.atan2(-l,d),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+e)}return this._order=e,n===!0&&this._onChangeCallback(),this}setFromQuaternion(t,e,n){return Is.makeRotationFromQuaternion(t),this.setFromRotationMatrix(Is,e,n)}setFromVector3(t,e=this._order){return this.set(t.x,t.y,t.z,e)}reorder(t){return Ps.setFromEuler(this),this.setFromQuaternion(Ps,t)}equals(t){return t._x===this._x&&t._y===this._y&&t._z===this._z&&t._order===this._order}fromArray(t){return this._x=t[0],this._y=t[1],this._z=t[2],t[3]!==void 0&&(this._order=t[3]),this._onChangeCallback(),this}toArray(t=[],e=0){return t[e]=this._x,t[e+1]=this._y,t[e+2]=this._z,t[e+3]=this._order,t}_onChange(t){return this._onChangeCallback=t,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}};We.DEFAULT_ORDER="XYZ";var bn=class{constructor(){this.mask=1}set(t){this.mask=(1<<t|0)>>>0}enable(t){this.mask|=1<<t|0}enableAll(){this.mask=-1}toggle(t){this.mask^=1<<t|0}disable(t){this.mask&=~(1<<t|0)}disableAll(){this.mask=0}test(t){return(this.mask&t.mask)!==0}isEnabled(t){return(this.mask&(1<<t|0))!==0}},Kr=0,Ds=new S,he=new Pt,wt=new q,fn=new S,Oe=new S,Qr=new S,jr=new Pt,Ls=new S(1,0,0),Us=new S(0,1,0),Ns=new S(0,0,1),Fs={type:"added"},to={type:"removed"},fe={type:"childadded",child:null},_i={type:"childremoved",child:null},Qt=class h extends ye{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:Kr++}),this.uuid=Bn(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=h.DEFAULT_UP.clone();let t=new S,e=new We,n=new Pt,i=new S(1,1,1);function s(){n.setFromEuler(e,!1)}function r(){e.setFromQuaternion(n,void 0,!1)}e._onChange(s),n._onChange(r),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:t},rotation:{configurable:!0,enumerable:!0,value:e},quaternion:{configurable:!0,enumerable:!0,value:n},scale:{configurable:!0,enumerable:!0,value:i},modelViewMatrix:{value:new q},normalMatrix:{value:new N}}),this.matrix=new q,this.matrixWorld=new q,this.matrixAutoUpdate=h.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=h.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new bn,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.customDepthMaterial=void 0,this.customDistanceMaterial=void 0,this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(t){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(t),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(t){return this.quaternion.premultiply(t),this}setRotationFromAxisAngle(t,e){this.quaternion.setFromAxisAngle(t,e)}setRotationFromEuler(t){this.quaternion.setFromEuler(t,!0)}setRotationFromMatrix(t){this.quaternion.setFromRotationMatrix(t)}setRotationFromQuaternion(t){this.quaternion.copy(t)}rotateOnAxis(t,e){return he.setFromAxisAngle(t,e),this.quaternion.multiply(he),this}rotateOnWorldAxis(t,e){return he.setFromAxisAngle(t,e),this.quaternion.premultiply(he),this}rotateX(t){return this.rotateOnAxis(Ls,t)}rotateY(t){return this.rotateOnAxis(Us,t)}rotateZ(t){return this.rotateOnAxis(Ns,t)}translateOnAxis(t,e){return Ds.copy(t).applyQuaternion(this.quaternion),this.position.add(Ds.multiplyScalar(e)),this}translateX(t){return this.translateOnAxis(Ls,t)}translateY(t){return this.translateOnAxis(Us,t)}translateZ(t){return this.translateOnAxis(Ns,t)}localToWorld(t){return this.updateWorldMatrix(!0,!1),t.applyMatrix4(this.matrixWorld)}worldToLocal(t){return this.updateWorldMatrix(!0,!1),t.applyMatrix4(wt.copy(this.matrixWorld).invert())}lookAt(t,e,n){t.isVector3?fn.copy(t):fn.set(t,e,n);let i=this.parent;this.updateWorldMatrix(!0,!1),Oe.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?wt.lookAt(Oe,fn,this.up):wt.lookAt(fn,Oe,this.up),this.quaternion.setFromRotationMatrix(wt),i&&(wt.extractRotation(i.matrixWorld),he.setFromRotationMatrix(wt),this.quaternion.premultiply(he.invert()))}add(t){if(arguments.length>1){for(let e=0;e<arguments.length;e++)this.add(arguments[e]);return this}return t===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",t),this):(t&&t.isObject3D?(t.removeFromParent(),t.parent=this,this.children.push(t),t.dispatchEvent(Fs),fe.child=t,this.dispatchEvent(fe),fe.child=null):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",t),this)}remove(t){if(arguments.length>1){for(let n=0;n<arguments.length;n++)this.remove(arguments[n]);return this}let e=this.children.indexOf(t);return e!==-1&&(t.parent=null,this.children.splice(e,1),t.dispatchEvent(to),_i.child=t,this.dispatchEvent(_i),_i.child=null),this}removeFromParent(){let t=this.parent;return t!==null&&t.remove(this),this}clear(){return this.remove(...this.children)}attach(t){return this.updateWorldMatrix(!0,!1),wt.copy(this.matrixWorld).invert(),t.parent!==null&&(t.parent.updateWorldMatrix(!0,!1),wt.multiply(t.parent.matrixWorld)),t.applyMatrix4(wt),t.removeFromParent(),t.parent=this,this.children.push(t),t.updateWorldMatrix(!1,!0),t.dispatchEvent(Fs),fe.child=t,this.dispatchEvent(fe),fe.child=null,this}getObjectById(t){return this.getObjectByProperty("id",t)}getObjectByName(t){return this.getObjectByProperty("name",t)}getObjectByProperty(t,e){if(this[t]===e)return this;for(let n=0,i=this.children.length;n<i;n++){let r=this.children[n].getObjectByProperty(t,e);if(r!==void 0)return r}}getObjectsByProperty(t,e,n=[]){this[t]===e&&n.push(this);let i=this.children;for(let s=0,r=i.length;s<r;s++)i[s].getObjectsByProperty(t,e,n);return n}getWorldPosition(t){return this.updateWorldMatrix(!0,!1),t.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(t){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Oe,t,Qr),t}getWorldScale(t){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Oe,jr,t),t}getWorldDirection(t){this.updateWorldMatrix(!0,!1);let e=this.matrixWorld.elements;return t.set(e[8],e[9],e[10]).normalize()}raycast(){}traverse(t){t(this);let e=this.children;for(let n=0,i=e.length;n<i;n++)e[n].traverse(t)}traverseVisible(t){if(this.visible===!1)return;t(this);let e=this.children;for(let n=0,i=e.length;n<i;n++)e[n].traverseVisible(t)}traverseAncestors(t){let e=this.parent;e!==null&&(t(e),e.traverseAncestors(t))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(t){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||t)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,t=!0);let e=this.children;for(let n=0,i=e.length;n<i;n++)e[n].updateMatrixWorld(t)}updateWorldMatrix(t,e){let n=this.parent;if(t===!0&&n!==null&&n.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),e===!0){let i=this.children;for(let s=0,r=i.length;s<r;s++)i[s].updateWorldMatrix(!1,!0)}}toJSON(t){let e=t===void 0||typeof t=="string",n={};e&&(t={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},n.metadata={version:4.7,type:"Object",generator:"Object3D.toJSON"});let i={};i.uuid=this.uuid,i.type=this.type,this.name!==""&&(i.name=this.name),this.castShadow===!0&&(i.castShadow=!0),this.receiveShadow===!0&&(i.receiveShadow=!0),this.visible===!1&&(i.visible=!1),this.frustumCulled===!1&&(i.frustumCulled=!1),this.renderOrder!==0&&(i.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(i.userData=this.userData),i.layers=this.layers.mask,i.matrix=this.matrix.toArray(),i.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(i.matrixAutoUpdate=!1),this.isInstancedMesh&&(i.type="InstancedMesh",i.count=this.count,i.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(i.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(i.type="BatchedMesh",i.perObjectFrustumCulled=this.perObjectFrustumCulled,i.sortObjects=this.sortObjects,i.drawRanges=this._drawRanges,i.reservedRanges=this._reservedRanges,i.geometryInfo=this._geometryInfo.map(o=>({...o,boundingBox:o.boundingBox?o.boundingBox.toJSON():void 0,boundingSphere:o.boundingSphere?o.boundingSphere.toJSON():void 0})),i.instanceInfo=this._instanceInfo.map(o=>({...o})),i.availableInstanceIds=this._availableInstanceIds.slice(),i.availableGeometryIds=this._availableGeometryIds.slice(),i.nextIndexStart=this._nextIndexStart,i.nextVertexStart=this._nextVertexStart,i.geometryCount=this._geometryCount,i.maxInstanceCount=this._maxInstanceCount,i.maxVertexCount=this._maxVertexCount,i.maxIndexCount=this._maxIndexCount,i.geometryInitialized=this._geometryInitialized,i.matricesTexture=this._matricesTexture.toJSON(t),i.indirectTexture=this._indirectTexture.toJSON(t),this._colorsTexture!==null&&(i.colorsTexture=this._colorsTexture.toJSON(t)),this.boundingSphere!==null&&(i.boundingSphere=this.boundingSphere.toJSON()),this.boundingBox!==null&&(i.boundingBox=this.boundingBox.toJSON()));function s(o,a){return o[a.uuid]===void 0&&(o[a.uuid]=a.toJSON(t)),a.uuid}if(this.isScene)this.background&&(this.background.isColor?i.background=this.background.toJSON():this.background.isTexture&&(i.background=this.background.toJSON(t).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(i.environment=this.environment.toJSON(t).uuid);else if(this.isMesh||this.isLine||this.isPoints){i.geometry=s(t.geometries,this.geometry);let o=this.geometry.parameters;if(o!==void 0&&o.shapes!==void 0){let a=o.shapes;if(Array.isArray(a))for(let c=0,l=a.length;c<l;c++){let f=a[c];s(t.shapes,f)}else s(t.shapes,a)}}if(this.isSkinnedMesh&&(i.bindMode=this.bindMode,i.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(s(t.skeletons,this.skeleton),i.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){let o=[];for(let a=0,c=this.material.length;a<c;a++)o.push(s(t.materials,this.material[a]));i.material=o}else i.material=s(t.materials,this.material);if(this.children.length>0){i.children=[];for(let o=0;o<this.children.length;o++)i.children.push(this.children[o].toJSON(t).object)}if(this.animations.length>0){i.animations=[];for(let o=0;o<this.animations.length;o++){let a=this.animations[o];i.animations.push(s(t.animations,a))}}if(e){let o=r(t.geometries),a=r(t.materials),c=r(t.textures),l=r(t.images),f=r(t.shapes),u=r(t.skeletons),d=r(t.animations),p=r(t.nodes);o.length>0&&(n.geometries=o),a.length>0&&(n.materials=a),c.length>0&&(n.textures=c),l.length>0&&(n.images=l),f.length>0&&(n.shapes=f),u.length>0&&(n.skeletons=u),d.length>0&&(n.animations=d),p.length>0&&(n.nodes=p)}return n.object=i,n;function r(o){let a=[];for(let c in o){let l=o[c];delete l.metadata,a.push(l)}return a}}clone(t){return new this.constructor().copy(this,t)}copy(t,e=!0){if(this.name=t.name,this.up.copy(t.up),this.position.copy(t.position),this.rotation.order=t.rotation.order,this.quaternion.copy(t.quaternion),this.scale.copy(t.scale),this.matrix.copy(t.matrix),this.matrixWorld.copy(t.matrixWorld),this.matrixAutoUpdate=t.matrixAutoUpdate,this.matrixWorldAutoUpdate=t.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=t.matrixWorldNeedsUpdate,this.layers.mask=t.layers.mask,this.visible=t.visible,this.castShadow=t.castShadow,this.receiveShadow=t.receiveShadow,this.frustumCulled=t.frustumCulled,this.renderOrder=t.renderOrder,this.animations=t.animations.slice(),this.userData=JSON.parse(JSON.stringify(t.userData)),e===!0)for(let n=0;n<t.children.length;n++){let i=t.children[n];this.add(i.clone())}return this}};Qt.DEFAULT_UP=new S(0,1,0);Qt.DEFAULT_MATRIX_AUTO_UPDATE=!0;Qt.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;var Mt=new S,Ct=new S,xi=new S,Rt=new S,de=new S,pe=new S,Bs=new S,yi=new S,vi=new S,Mi=new S,Si=new Me,bi=new Me,Ti=new Me,St=class h{constructor(t=new S,e=new S,n=new S){this.a=t,this.b=e,this.c=n}static getNormal(t,e,n,i){i.subVectors(n,e),Mt.subVectors(t,e),i.cross(Mt);let s=i.lengthSq();return s>0?i.multiplyScalar(1/Math.sqrt(s)):i.set(0,0,0)}static getBarycoord(t,e,n,i,s){Mt.subVectors(i,e),Ct.subVectors(n,e),xi.subVectors(t,e);let r=Mt.dot(Mt),o=Mt.dot(Ct),a=Mt.dot(xi),c=Ct.dot(Ct),l=Ct.dot(xi),f=r*c-o*o;if(f===0)return s.set(0,0,0),null;let u=1/f,d=(c*a-o*l)*u,p=(r*l-o*a)*u;return s.set(1-d-p,p,d)}static containsPoint(t,e,n,i){return this.getBarycoord(t,e,n,i,Rt)===null?!1:Rt.x>=0&&Rt.y>=0&&Rt.x+Rt.y<=1}static getInterpolation(t,e,n,i,s,r,o,a){return this.getBarycoord(t,e,n,i,Rt)===null?(a.x=0,a.y=0,"z"in a&&(a.z=0),"w"in a&&(a.w=0),null):(a.setScalar(0),a.addScaledVector(s,Rt.x),a.addScaledVector(r,Rt.y),a.addScaledVector(o,Rt.z),a)}static getInterpolatedAttribute(t,e,n,i,s,r){return Si.setScalar(0),bi.setScalar(0),Ti.setScalar(0),Si.fromBufferAttribute(t,e),bi.fromBufferAttribute(t,n),Ti.fromBufferAttribute(t,i),r.setScalar(0),r.addScaledVector(Si,s.x),r.addScaledVector(bi,s.y),r.addScaledVector(Ti,s.z),r}static isFrontFacing(t,e,n,i){return Mt.subVectors(n,e),Ct.subVectors(t,e),Mt.cross(Ct).dot(i)<0}set(t,e,n){return this.a.copy(t),this.b.copy(e),this.c.copy(n),this}setFromPointsAndIndices(t,e,n,i){return this.a.copy(t[e]),this.b.copy(t[n]),this.c.copy(t[i]),this}setFromAttributeAndIndices(t,e,n,i){return this.a.fromBufferAttribute(t,e),this.b.fromBufferAttribute(t,n),this.c.fromBufferAttribute(t,i),this}clone(){return new this.constructor().copy(this)}copy(t){return this.a.copy(t.a),this.b.copy(t.b),this.c.copy(t.c),this}getArea(){return Mt.subVectors(this.c,this.b),Ct.subVectors(this.a,this.b),Mt.cross(Ct).length()*.5}getMidpoint(t){return t.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(t){return h.getNormal(this.a,this.b,this.c,t)}getPlane(t){return t.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(t,e){return h.getBarycoord(t,this.a,this.b,this.c,e)}getInterpolation(t,e,n,i,s){return h.getInterpolation(t,this.a,this.b,this.c,e,n,i,s)}containsPoint(t){return h.containsPoint(t,this.a,this.b,this.c)}isFrontFacing(t){return h.isFrontFacing(this.a,this.b,this.c,t)}intersectsBox(t){return t.intersectsTriangle(this)}closestPointToPoint(t,e){let n=this.a,i=this.b,s=this.c,r,o;de.subVectors(i,n),pe.subVectors(s,n),yi.subVectors(t,n);let a=de.dot(yi),c=pe.dot(yi);if(a<=0&&c<=0)return e.copy(n);vi.subVectors(t,i);let l=de.dot(vi),f=pe.dot(vi);if(l>=0&&f<=l)return e.copy(i);let u=a*f-l*c;if(u<=0&&a>=0&&l<=0)return r=a/(a-l),e.copy(n).addScaledVector(de,r);Mi.subVectors(t,s);let d=de.dot(Mi),p=pe.dot(Mi);if(p>=0&&d<=p)return e.copy(s);let m=d*c-a*p;if(m<=0&&c>=0&&p<=0)return o=c/(c-p),e.copy(n).addScaledVector(pe,o);let v=l*p-d*f;if(v<=0&&f-l>=0&&d-p>=0)return Bs.subVectors(s,i),o=(f-l)/(f-l+(d-p)),e.copy(i).addScaledVector(Bs,o);let y=1/(v+m+u);return r=m*y,o=u*y,e.copy(n).addScaledVector(de,r).addScaledVector(pe,o)}equals(t){return t.a.equals(this.a)&&t.b.equals(this.b)&&t.c.equals(this.c)}},Xs={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},Vt={h:0,s:0,l:0},dn={h:0,s:0,l:0};function Ei(h,t,e){return e<0&&(e+=1),e>1&&(e-=1),e<1/6?h+(t-h)*6*e:e<1/2?t:e<2/3?h+(t-h)*6*(2/3-e):h}var tt=class{constructor(t,e,n){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(t,e,n)}set(t,e,n){if(e===void 0&&n===void 0){let i=t;i&&i.isColor?this.copy(i):typeof i=="number"?this.setHex(i):typeof i=="string"&&this.setStyle(i)}else this.setRGB(t,e,n);return this}setScalar(t){return this.r=t,this.g=t,this.b=t,this}setHex(t,e=gt){return t=Math.floor(t),this.r=(t>>16&255)/255,this.g=(t>>8&255)/255,this.b=(t&255)/255,mt.colorSpaceToWorking(this,e),this}setRGB(t,e,n,i=mt.workingColorSpace){return this.r=t,this.g=e,this.b=n,mt.colorSpaceToWorking(this,i),this}setHSL(t,e,n,i=mt.workingColorSpace){if(t=Wr(t,1),e=U(e,0,1),n=U(n,0,1),e===0)this.r=this.g=this.b=n;else{let s=n<=.5?n*(1+e):n+e-n*e,r=2*n-s;this.r=Ei(r,s,t+1/3),this.g=Ei(r,s,t),this.b=Ei(r,s,t-1/3)}return mt.colorSpaceToWorking(this,i),this}setStyle(t,e=gt){function n(s){s!==void 0&&parseFloat(s)<1&&console.warn("THREE.Color: Alpha component of "+t+" will be ignored.")}let i;if(i=/^(\w+)\(([^\)]*)\)/.exec(t)){let s,r=i[1],o=i[2];switch(r){case"rgb":case"rgba":if(s=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return n(s[4]),this.setRGB(Math.min(255,parseInt(s[1],10))/255,Math.min(255,parseInt(s[2],10))/255,Math.min(255,parseInt(s[3],10))/255,e);if(s=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return n(s[4]),this.setRGB(Math.min(100,parseInt(s[1],10))/100,Math.min(100,parseInt(s[2],10))/100,Math.min(100,parseInt(s[3],10))/100,e);break;case"hsl":case"hsla":if(s=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return n(s[4]),this.setHSL(parseFloat(s[1])/360,parseFloat(s[2])/100,parseFloat(s[3])/100,e);break;default:console.warn("THREE.Color: Unknown color model "+t)}}else if(i=/^\#([A-Fa-f\d]+)$/.exec(t)){let s=i[1],r=s.length;if(r===3)return this.setRGB(parseInt(s.charAt(0),16)/15,parseInt(s.charAt(1),16)/15,parseInt(s.charAt(2),16)/15,e);if(r===6)return this.setHex(parseInt(s,16),e);console.warn("THREE.Color: Invalid hex color "+t)}else if(t&&t.length>0)return this.setColorName(t,e);return this}setColorName(t,e=gt){let n=Xs[t.toLowerCase()];return n!==void 0?this.setHex(n,e):console.warn("THREE.Color: Unknown color "+t),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(t){return this.r=t.r,this.g=t.g,this.b=t.b,this}copySRGBToLinear(t){return this.r=It(t.r),this.g=It(t.g),this.b=It(t.b),this}copyLinearToSRGB(t){return this.r=xe(t.r),this.g=xe(t.g),this.b=xe(t.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(t=gt){return mt.workingToColorSpace(it.copy(this),t),Math.round(U(it.r*255,0,255))*65536+Math.round(U(it.g*255,0,255))*256+Math.round(U(it.b*255,0,255))}getHexString(t=gt){return("000000"+this.getHex(t).toString(16)).slice(-6)}getHSL(t,e=mt.workingColorSpace){mt.workingToColorSpace(it.copy(this),e);let n=it.r,i=it.g,s=it.b,r=Math.max(n,i,s),o=Math.min(n,i,s),a,c,l=(o+r)/2;if(o===r)a=0,c=0;else{let f=r-o;switch(c=l<=.5?f/(r+o):f/(2-r-o),r){case n:a=(i-s)/f+(i<s?6:0);break;case i:a=(s-n)/f+2;break;case s:a=(n-i)/f+4;break}a/=6}return t.h=a,t.s=c,t.l=l,t}getRGB(t,e=mt.workingColorSpace){return mt.workingToColorSpace(it.copy(this),e),t.r=it.r,t.g=it.g,t.b=it.b,t}getStyle(t=gt){mt.workingToColorSpace(it.copy(this),t);let e=it.r,n=it.g,i=it.b;return t!==gt?`color(${t} ${e.toFixed(3)} ${n.toFixed(3)} ${i.toFixed(3)})`:`rgb(${Math.round(e*255)},${Math.round(n*255)},${Math.round(i*255)})`}offsetHSL(t,e,n){return this.getHSL(Vt),this.setHSL(Vt.h+t,Vt.s+e,Vt.l+n)}add(t){return this.r+=t.r,this.g+=t.g,this.b+=t.b,this}addColors(t,e){return this.r=t.r+e.r,this.g=t.g+e.g,this.b=t.b+e.b,this}addScalar(t){return this.r+=t,this.g+=t,this.b+=t,this}sub(t){return this.r=Math.max(0,this.r-t.r),this.g=Math.max(0,this.g-t.g),this.b=Math.max(0,this.b-t.b),this}multiply(t){return this.r*=t.r,this.g*=t.g,this.b*=t.b,this}multiplyScalar(t){return this.r*=t,this.g*=t,this.b*=t,this}lerp(t,e){return this.r+=(t.r-this.r)*e,this.g+=(t.g-this.g)*e,this.b+=(t.b-this.b)*e,this}lerpColors(t,e,n){return this.r=t.r+(e.r-t.r)*n,this.g=t.g+(e.g-t.g)*n,this.b=t.b+(e.b-t.b)*n,this}lerpHSL(t,e){this.getHSL(Vt),t.getHSL(dn);let n=ai(Vt.h,dn.h,e),i=ai(Vt.s,dn.s,e),s=ai(Vt.l,dn.l,e);return this.setHSL(n,i,s),this}setFromVector3(t){return this.r=t.x,this.g=t.y,this.b=t.z,this}applyMatrix3(t){let e=this.r,n=this.g,i=this.b,s=t.elements;return this.r=s[0]*e+s[3]*n+s[6]*i,this.g=s[1]*e+s[4]*n+s[7]*i,this.b=s[2]*e+s[5]*n+s[8]*i,this}equals(t){return t.r===this.r&&t.g===this.g&&t.b===this.b}fromArray(t,e=0){return this.r=t[e],this.g=t[e+1],this.b=t[e+2],this}toArray(t=[],e=0){return t[e]=this.r,t[e+1]=this.g,t[e+2]=this.b,t}fromBufferAttribute(t,e){return this.r=t.getX(e),this.g=t.getY(e),this.b=t.getZ(e),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}},it=new tt;tt.NAMES=Xs;var $=new S,pn=new G,eo=0,st=class{constructor(t,e,n=!1){if(Array.isArray(t))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:eo++}),this.name="",this.array=t,this.itemSize=e,this.count=t!==void 0?t.length/e:0,this.normalized=n,this.usage=Fi,this.updateRanges=[],this.gpuType=Hs,this.version=0}onUploadCallback(){}set needsUpdate(t){t===!0&&this.version++}setUsage(t){return this.usage=t,this}addUpdateRange(t,e){this.updateRanges.push({start:t,count:e})}clearUpdateRanges(){this.updateRanges.length=0}copy(t){return this.name=t.name,this.array=new t.array.constructor(t.array),this.itemSize=t.itemSize,this.count=t.count,this.normalized=t.normalized,this.usage=t.usage,this.gpuType=t.gpuType,this}copyAt(t,e,n){t*=this.itemSize,n*=e.itemSize;for(let i=0,s=this.itemSize;i<s;i++)this.array[t+i]=e.array[n+i];return this}copyArray(t){return this.array.set(t),this}applyMatrix3(t){if(this.itemSize===2)for(let e=0,n=this.count;e<n;e++)pn.fromBufferAttribute(this,e),pn.applyMatrix3(t),this.setXY(e,pn.x,pn.y);else if(this.itemSize===3)for(let e=0,n=this.count;e<n;e++)$.fromBufferAttribute(this,e),$.applyMatrix3(t),this.setXYZ(e,$.x,$.y,$.z);return this}applyMatrix4(t){for(let e=0,n=this.count;e<n;e++)$.fromBufferAttribute(this,e),$.applyMatrix4(t),this.setXYZ(e,$.x,$.y,$.z);return this}applyNormalMatrix(t){for(let e=0,n=this.count;e<n;e++)$.fromBufferAttribute(this,e),$.applyNormalMatrix(t),this.setXYZ(e,$.x,$.y,$.z);return this}transformDirection(t){for(let e=0,n=this.count;e<n;e++)$.fromBufferAttribute(this,e),$.transformDirection(t),this.setXYZ(e,$.x,$.y,$.z);return this}set(t,e=0){return this.array.set(t,e),this}getComponent(t,e){let n=this.array[t*this.itemSize+e];return this.normalized&&(n=Ne(n,this.array)),n}setComponent(t,e,n){return this.normalized&&(n=lt(n,this.array)),this.array[t*this.itemSize+e]=n,this}getX(t){let e=this.array[t*this.itemSize];return this.normalized&&(e=Ne(e,this.array)),e}setX(t,e){return this.normalized&&(e=lt(e,this.array)),this.array[t*this.itemSize]=e,this}getY(t){let e=this.array[t*this.itemSize+1];return this.normalized&&(e=Ne(e,this.array)),e}setY(t,e){return this.normalized&&(e=lt(e,this.array)),this.array[t*this.itemSize+1]=e,this}getZ(t){let e=this.array[t*this.itemSize+2];return this.normalized&&(e=Ne(e,this.array)),e}setZ(t,e){return this.normalized&&(e=lt(e,this.array)),this.array[t*this.itemSize+2]=e,this}getW(t){let e=this.array[t*this.itemSize+3];return this.normalized&&(e=Ne(e,this.array)),e}setW(t,e){return this.normalized&&(e=lt(e,this.array)),this.array[t*this.itemSize+3]=e,this}setXY(t,e,n){return t*=this.itemSize,this.normalized&&(e=lt(e,this.array),n=lt(n,this.array)),this.array[t+0]=e,this.array[t+1]=n,this}setXYZ(t,e,n,i){return t*=this.itemSize,this.normalized&&(e=lt(e,this.array),n=lt(n,this.array),i=lt(i,this.array)),this.array[t+0]=e,this.array[t+1]=n,this.array[t+2]=i,this}setXYZW(t,e,n,i,s){return t*=this.itemSize,this.normalized&&(e=lt(e,this.array),n=lt(n,this.array),i=lt(i,this.array),s=lt(s,this.array)),this.array[t+0]=e,this.array[t+1]=n,this.array[t+2]=i,this.array[t+3]=s,this}onUpload(t){return this.onUploadCallback=t,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){let t={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(t.name=this.name),this.usage!==Fi&&(t.usage=this.usage),t}};var Tn=class extends st{constructor(t,e,n){super(new Uint16Array(t),e,n)}};var En=class extends st{constructor(t,e,n){super(new Uint32Array(t),e,n)}};var An=class extends st{constructor(t,e,n){super(new Float32Array(t),e,n)}},no=0,pt=new q,Ai=new Qt,me=new S,ht=new Y,ze=new Y,j=new S,Xe=class h extends ye{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:no++}),this.uuid=Bn(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(t){return Array.isArray(t)?this.index=new(Ws(t)?En:Tn)(t,1):this.index=t,this}setIndirect(t){return this.indirect=t,this}getIndirect(){return this.indirect}getAttribute(t){return this.attributes[t]}setAttribute(t,e){return this.attributes[t]=e,this}deleteAttribute(t){return delete this.attributes[t],this}hasAttribute(t){return this.attributes[t]!==void 0}addGroup(t,e,n=0){this.groups.push({start:t,count:e,materialIndex:n})}clearGroups(){this.groups=[]}setDrawRange(t,e){this.drawRange.start=t,this.drawRange.count=e}applyMatrix4(t){let e=this.attributes.position;e!==void 0&&(e.applyMatrix4(t),e.needsUpdate=!0);let n=this.attributes.normal;if(n!==void 0){let s=new N().getNormalMatrix(t);n.applyNormalMatrix(s),n.needsUpdate=!0}let i=this.attributes.tangent;return i!==void 0&&(i.transformDirection(t),i.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(t){return pt.makeRotationFromQuaternion(t),this.applyMatrix4(pt),this}rotateX(t){return pt.makeRotationX(t),this.applyMatrix4(pt),this}rotateY(t){return pt.makeRotationY(t),this.applyMatrix4(pt),this}rotateZ(t){return pt.makeRotationZ(t),this.applyMatrix4(pt),this}translate(t,e,n){return pt.makeTranslation(t,e,n),this.applyMatrix4(pt),this}scale(t,e,n){return pt.makeScale(t,e,n),this.applyMatrix4(pt),this}lookAt(t){return Ai.lookAt(t),Ai.updateMatrix(),this.applyMatrix4(Ai.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(me).negate(),this.translate(me.x,me.y,me.z),this}setFromPoints(t){let e=this.getAttribute("position");if(e===void 0){let n=[];for(let i=0,s=t.length;i<s;i++){let r=t[i];n.push(r.x,r.y,r.z||0)}this.setAttribute("position",new An(n,3))}else{let n=Math.min(t.length,e.count);for(let i=0;i<n;i++){let s=t[i];e.setXYZ(i,s.x,s.y,s.z||0)}t.length>e.count&&console.warn("THREE.BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),e.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Y);let t=this.attributes.position,e=this.morphAttributes.position;if(t&&t.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new S(-1/0,-1/0,-1/0),new S(1/0,1/0,1/0));return}if(t!==void 0){if(this.boundingBox.setFromBufferAttribute(t),e)for(let n=0,i=e.length;n<i;n++){let s=e[n];ht.setFromBufferAttribute(s),this.morphTargetsRelative?(j.addVectors(this.boundingBox.min,ht.min),this.boundingBox.expandByPoint(j),j.addVectors(this.boundingBox.max,ht.max),this.boundingBox.expandByPoint(j)):(this.boundingBox.expandByPoint(ht.min),this.boundingBox.expandByPoint(ht.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Sn);let t=this.attributes.position,e=this.morphAttributes.position;if(t&&t.isGLBufferAttribute){console.error("THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new S,1/0);return}if(t){let n=this.boundingSphere.center;if(ht.setFromBufferAttribute(t),e)for(let s=0,r=e.length;s<r;s++){let o=e[s];ze.setFromBufferAttribute(o),this.morphTargetsRelative?(j.addVectors(ht.min,ze.min),ht.expandByPoint(j),j.addVectors(ht.max,ze.max),ht.expandByPoint(j)):(ht.expandByPoint(ze.min),ht.expandByPoint(ze.max))}ht.getCenter(n);let i=0;for(let s=0,r=t.count;s<r;s++)j.fromBufferAttribute(t,s),i=Math.max(i,n.distanceToSquared(j));if(e)for(let s=0,r=e.length;s<r;s++){let o=e[s],a=this.morphTargetsRelative;for(let c=0,l=o.count;c<l;c++)j.fromBufferAttribute(o,c),a&&(me.fromBufferAttribute(t,c),j.add(me)),i=Math.max(i,n.distanceToSquared(j))}this.boundingSphere.radius=Math.sqrt(i),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){let t=this.index,e=this.attributes;if(t===null||e.position===void 0||e.normal===void 0||e.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}let n=e.position,i=e.normal,s=e.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new st(new Float32Array(4*n.count),4));let r=this.getAttribute("tangent"),o=[],a=[];for(let T=0;T<n.count;T++)o[T]=new S,a[T]=new S;let c=new S,l=new S,f=new S,u=new G,d=new G,p=new G,m=new S,v=new S;function y(T,C,A){c.fromBufferAttribute(n,T),l.fromBufferAttribute(n,C),f.fromBufferAttribute(n,A),u.fromBufferAttribute(s,T),d.fromBufferAttribute(s,C),p.fromBufferAttribute(s,A),l.sub(c),f.sub(c),d.sub(u),p.sub(u);let R=1/(d.x*p.y-p.x*d.y);isFinite(R)&&(m.copy(l).multiplyScalar(p.y).addScaledVector(f,-d.y).multiplyScalar(R),v.copy(f).multiplyScalar(d.x).addScaledVector(l,-p.x).multiplyScalar(R),o[T].add(m),o[C].add(m),o[A].add(m),a[T].add(v),a[C].add(v),a[A].add(v))}let g=this.groups;g.length===0&&(g=[{start:0,count:t.count}]);for(let T=0,C=g.length;T<C;++T){let A=g[T],R=A.start,w=A.count;for(let I=R,D=R+w;I<D;I+=3)y(t.getX(I+0),t.getX(I+1),t.getX(I+2))}let M=new S,x=new S,_=new S,E=new S;function b(T){_.fromBufferAttribute(i,T),E.copy(_);let C=o[T];M.copy(C),M.sub(_.multiplyScalar(_.dot(C))).normalize(),x.crossVectors(E,C);let R=x.dot(a[T])<0?-1:1;r.setXYZW(T,M.x,M.y,M.z,R)}for(let T=0,C=g.length;T<C;++T){let A=g[T],R=A.start,w=A.count;for(let I=R,D=R+w;I<D;I+=3)b(t.getX(I+0)),b(t.getX(I+1)),b(t.getX(I+2))}}computeVertexNormals(){let t=this.index,e=this.getAttribute("position");if(e!==void 0){let n=this.getAttribute("normal");if(n===void 0)n=new st(new Float32Array(e.count*3),3),this.setAttribute("normal",n);else for(let u=0,d=n.count;u<d;u++)n.setXYZ(u,0,0,0);let i=new S,s=new S,r=new S,o=new S,a=new S,c=new S,l=new S,f=new S;if(t)for(let u=0,d=t.count;u<d;u+=3){let p=t.getX(u+0),m=t.getX(u+1),v=t.getX(u+2);i.fromBufferAttribute(e,p),s.fromBufferAttribute(e,m),r.fromBufferAttribute(e,v),l.subVectors(r,s),f.subVectors(i,s),l.cross(f),o.fromBufferAttribute(n,p),a.fromBufferAttribute(n,m),c.fromBufferAttribute(n,v),o.add(l),a.add(l),c.add(l),n.setXYZ(p,o.x,o.y,o.z),n.setXYZ(m,a.x,a.y,a.z),n.setXYZ(v,c.x,c.y,c.z)}else for(let u=0,d=e.count;u<d;u+=3)i.fromBufferAttribute(e,u+0),s.fromBufferAttribute(e,u+1),r.fromBufferAttribute(e,u+2),l.subVectors(r,s),f.subVectors(i,s),l.cross(f),n.setXYZ(u+0,l.x,l.y,l.z),n.setXYZ(u+1,l.x,l.y,l.z),n.setXYZ(u+2,l.x,l.y,l.z);this.normalizeNormals(),n.needsUpdate=!0}}normalizeNormals(){let t=this.attributes.normal;for(let e=0,n=t.count;e<n;e++)j.fromBufferAttribute(t,e),j.normalize(),t.setXYZ(e,j.x,j.y,j.z)}toNonIndexed(){function t(o,a){let c=o.array,l=o.itemSize,f=o.normalized,u=new c.constructor(a.length*l),d=0,p=0;for(let m=0,v=a.length;m<v;m++){o.isInterleavedBufferAttribute?d=a[m]*o.data.stride+o.offset:d=a[m]*l;for(let y=0;y<l;y++)u[p++]=c[d++]}return new st(u,l,f)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;let e=new h,n=this.index.array,i=this.attributes;for(let o in i){let a=i[o],c=t(a,n);e.setAttribute(o,c)}let s=this.morphAttributes;for(let o in s){let a=[],c=s[o];for(let l=0,f=c.length;l<f;l++){let u=c[l],d=t(u,n);a.push(d)}e.morphAttributes[o]=a}e.morphTargetsRelative=this.morphTargetsRelative;let r=this.groups;for(let o=0,a=r.length;o<a;o++){let c=r[o];e.addGroup(c.start,c.count,c.materialIndex)}return e}toJSON(){let t={metadata:{version:4.7,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(t.uuid=this.uuid,t.type=this.type,this.name!==""&&(t.name=this.name),Object.keys(this.userData).length>0&&(t.userData=this.userData),this.parameters!==void 0){let a=this.parameters;for(let c in a)a[c]!==void 0&&(t[c]=a[c]);return t}t.data={attributes:{}};let e=this.index;e!==null&&(t.data.index={type:e.array.constructor.name,array:Array.prototype.slice.call(e.array)});let n=this.attributes;for(let a in n){let c=n[a];t.data.attributes[a]=c.toJSON(t.data)}let i={},s=!1;for(let a in this.morphAttributes){let c=this.morphAttributes[a],l=[];for(let f=0,u=c.length;f<u;f++){let d=c[f];l.push(d.toJSON(t.data))}l.length>0&&(i[a]=l,s=!0)}s&&(t.data.morphAttributes=i,t.data.morphTargetsRelative=this.morphTargetsRelative);let r=this.groups;r.length>0&&(t.data.groups=JSON.parse(JSON.stringify(r)));let o=this.boundingSphere;return o!==null&&(t.data.boundingSphere=o.toJSON()),t}clone(){return new this.constructor().copy(this)}copy(t){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;let e={};this.name=t.name;let n=t.index;n!==null&&this.setIndex(n.clone());let i=t.attributes;for(let c in i){let l=i[c];this.setAttribute(c,l.clone(e))}let s=t.morphAttributes;for(let c in s){let l=[],f=s[c];for(let u=0,d=f.length;u<d;u++)l.push(f[u].clone(e));this.morphAttributes[c]=l}this.morphTargetsRelative=t.morphTargetsRelative;let r=t.groups;for(let c=0,l=r.length;c<l;c++){let f=r[c];this.addGroup(f.start,f.count,f.materialIndex)}let o=t.boundingBox;o!==null&&(this.boundingBox=o.clone());let a=t.boundingSphere;return a!==null&&(this.boundingSphere=a.clone()),this.drawRange.start=t.drawRange.start,this.drawRange.count=t.drawRange.count,this.userData=t.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}};function qs(h){let t={};for(let e in h){t[e]={};for(let n in h[e]){let i=h[e][n];i&&(i.isColor||i.isMatrix3||i.isMatrix4||i.isVector2||i.isVector3||i.isVector4||i.isTexture||i.isQuaternion)?i.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),t[e][n]=null):t[e][n]=i.clone():Array.isArray(i)?t[e][n]=i.slice():t[e][n]=i}}return t}function ot(h){let t={};for(let e=0;e<h.length;e++){let n=qs(h[e]);for(let i in n)t[i]=n[i]}return t}var wi=new S,io=new S,so=new N,jt=class{constructor(t=new S(1,0,0),e=0){this.isPlane=!0,this.normal=t,this.constant=e}set(t,e){return this.normal.copy(t),this.constant=e,this}setComponents(t,e,n,i){return this.normal.set(t,e,n),this.constant=i,this}setFromNormalAndCoplanarPoint(t,e){return this.normal.copy(t),this.constant=-e.dot(this.normal),this}setFromCoplanarPoints(t,e,n){let i=wi.subVectors(n,e).cross(io.subVectors(t,e)).normalize();return this.setFromNormalAndCoplanarPoint(i,t),this}copy(t){return this.normal.copy(t.normal),this.constant=t.constant,this}normalize(){let t=1/this.normal.length();return this.normal.multiplyScalar(t),this.constant*=t,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(t){return this.normal.dot(t)+this.constant}distanceToSphere(t){return this.distanceToPoint(t.center)-t.radius}projectPoint(t,e){return e.copy(t).addScaledVector(this.normal,-this.distanceToPoint(t))}intersectLine(t,e){let n=t.delta(wi),i=this.normal.dot(n);if(i===0)return this.distanceToPoint(t.start)===0?e.copy(t.start):null;let s=-(t.start.dot(this.normal)+this.constant)/i;return s<0||s>1?null:e.copy(t.start).addScaledVector(n,s)}intersectsLine(t){let e=this.distanceToPoint(t.start),n=this.distanceToPoint(t.end);return e<0&&n>0||n<0&&e>0}intersectsBox(t){return t.intersectsPlane(this)}intersectsSphere(t){return t.intersectsPlane(this)}coplanarPoint(t){return t.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(t,e){let n=e||so.getNormalMatrix(t),i=this.coplanarPoint(wi).applyMatrix4(t),s=this.normal.applyMatrix3(n).normalize();return this.constant=-i.dot(s),this}translate(t){return this.constant-=t.dot(this.normal),this}equals(t){return t.normal.equals(this.normal)&&t.constant===this.constant}clone(){return new this.constructor().copy(this)}};function mn(h,t){return!h||h.constructor===t?h:typeof t.BYTES_PER_ELEMENT=="number"?new t(h):Array.prototype.slice.call(h)}function ro(h){return ArrayBuffer.isView(h)&&!(h instanceof DataView)}var te=class{constructor(t,e,n,i){this.parameterPositions=t,this._cachedIndex=0,this.resultBuffer=i!==void 0?i:new e.constructor(n),this.sampleValues=e,this.valueSize=n,this.settings=null,this.DefaultSettings_={}}evaluate(t){let e=this.parameterPositions,n=this._cachedIndex,i=e[n],s=e[n-1];n:{t:{let r;e:{i:if(!(t<i)){for(let o=n+2;;){if(i===void 0){if(t<s)break i;return n=e.length,this._cachedIndex=n,this.copySampleValue_(n-1)}if(n===o)break;if(s=i,i=e[++n],t<i)break t}r=e.length;break e}if(!(t>=s)){let o=e[1];t<o&&(n=2,s=o);for(let a=n-2;;){if(s===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(n===a)break;if(i=s,s=e[--n-1],t>=s)break t}r=n,n=0;break e}break n}for(;n<r;){let o=n+r>>>1;t<e[o]?r=o:n=o+1}if(i=e[n],s=e[n-1],s===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(i===void 0)return n=e.length,this._cachedIndex=n,this.copySampleValue_(n-1)}this._cachedIndex=n,this.intervalChanged_(n,s,i)}return this.interpolate_(n,s,t,i)}getSettings_(){return this.settings||this.DefaultSettings_}copySampleValue_(t){let e=this.resultBuffer,n=this.sampleValues,i=this.valueSize,s=t*i;for(let r=0;r!==i;++r)e[r]=n[s+r];return e}interpolate_(){throw new Error("call to abstract method")}intervalChanged_(){}},wn=class extends te{constructor(t,e,n,i){super(t,e,n,i),this._weightPrev=-0,this._offsetPrev=-0,this._weightNext=-0,this._offsetNext=-0,this.DefaultSettings_={endingStart:Pi,endingEnd:Pi}}intervalChanged_(t,e,n){let i=this.parameterPositions,s=t-2,r=t+1,o=i[s],a=i[r];if(o===void 0)switch(this.getSettings_().endingStart){case Di:s=t,o=2*e-n;break;case Li:s=i.length-2,o=e+i[s]-i[s+1];break;default:s=t,o=n}if(a===void 0)switch(this.getSettings_().endingEnd){case Di:r=t,a=2*n-e;break;case Li:r=1,a=n+i[1]-i[0];break;default:r=t-1,a=e}let c=(n-e)*.5,l=this.valueSize;this._weightPrev=c/(e-o),this._weightNext=c/(a-n),this._offsetPrev=s*l,this._offsetNext=r*l}interpolate_(t,e,n,i){let s=this.resultBuffer,r=this.sampleValues,o=this.valueSize,a=t*o,c=a-o,l=this._offsetPrev,f=this._offsetNext,u=this._weightPrev,d=this._weightNext,p=(n-e)/(i-e),m=p*p,v=m*p,y=-u*v+2*u*m-u*p,g=(1+u)*v+(-1.5-2*u)*m+(-.5+u)*p+1,M=(-1-d)*v+(1.5+d)*m+.5*p,x=d*v-d*m;for(let _=0;_!==o;++_)s[_]=y*r[l+_]+g*r[c+_]+M*r[a+_]+x*r[f+_];return s}},Cn=class extends te{constructor(t,e,n,i){super(t,e,n,i)}interpolate_(t,e,n,i){let s=this.resultBuffer,r=this.sampleValues,o=this.valueSize,a=t*o,c=a-o,l=(n-e)/(i-e),f=1-l;for(let u=0;u!==o;++u)s[u]=r[c+u]*f+r[a+u]*l;return s}},Rn=class extends te{constructor(t,e,n,i){super(t,e,n,i)}interpolate_(t){return this.copySampleValue_(t-1)}},ft=class{constructor(t,e,n,i){if(t===void 0)throw new Error("THREE.KeyframeTrack: track name is undefined");if(e===void 0||e.length===0)throw new Error("THREE.KeyframeTrack: no keyframes in track named "+t);this.name=t,this.times=mn(e,this.TimeBufferType),this.values=mn(n,this.ValueBufferType),this.setInterpolation(i||this.DefaultInterpolation)}static toJSON(t){let e=t.constructor,n;if(e.toJSON!==this.toJSON)n=e.toJSON(t);else{n={name:t.name,times:mn(t.times,Array),values:mn(t.values,Array)};let i=t.getInterpolation();i!==t.DefaultInterpolation&&(n.interpolation=i)}return n.type=t.ValueTypeName,n}InterpolantFactoryMethodDiscrete(t){return new Rn(this.times,this.values,this.getValueSize(),t)}InterpolantFactoryMethodLinear(t){return new Cn(this.times,this.values,this.getValueSize(),t)}InterpolantFactoryMethodSmooth(t){return new wn(this.times,this.values,this.getValueSize(),t)}setInterpolation(t){let e;switch(t){case He:e=this.InterpolantFactoryMethodDiscrete;break;case yn:e=this.InterpolantFactoryMethodLinear;break;case _n:e=this.InterpolantFactoryMethodSmooth;break}if(e===void 0){let n="unsupported interpolation for "+this.ValueTypeName+" keyframe track named "+this.name;if(this.createInterpolant===void 0)if(t!==this.DefaultInterpolation)this.setInterpolation(this.DefaultInterpolation);else throw new Error(n);return console.warn("THREE.KeyframeTrack:",n),this}return this.createInterpolant=e,this}getInterpolation(){switch(this.createInterpolant){case this.InterpolantFactoryMethodDiscrete:return He;case this.InterpolantFactoryMethodLinear:return yn;case this.InterpolantFactoryMethodSmooth:return _n}}getValueSize(){return this.values.length/this.times.length}shift(t){if(t!==0){let e=this.times;for(let n=0,i=e.length;n!==i;++n)e[n]+=t}return this}scale(t){if(t!==1){let e=this.times;for(let n=0,i=e.length;n!==i;++n)e[n]*=t}return this}trim(t,e){let n=this.times,i=n.length,s=0,r=i-1;for(;s!==i&&n[s]<t;)++s;for(;r!==-1&&n[r]>e;)--r;if(++r,s!==0||r!==i){s>=r&&(r=Math.max(r,1),s=r-1);let o=this.getValueSize();this.times=n.slice(s,r),this.values=this.values.slice(s*o,r*o)}return this}validate(){let t=!0,e=this.getValueSize();e-Math.floor(e)!==0&&(console.error("THREE.KeyframeTrack: Invalid value size in track.",this),t=!1);let n=this.times,i=this.values,s=n.length;s===0&&(console.error("THREE.KeyframeTrack: Track is empty.",this),t=!1);let r=null;for(let o=0;o!==s;o++){let a=n[o];if(typeof a=="number"&&isNaN(a)){console.error("THREE.KeyframeTrack: Time is not a valid number.",this,o,a),t=!1;break}if(r!==null&&r>a){console.error("THREE.KeyframeTrack: Out of order keys.",this,o,a,r),t=!1;break}r=a}if(i!==void 0&&ro(i))for(let o=0,a=i.length;o!==a;++o){let c=i[o];if(isNaN(c)){console.error("THREE.KeyframeTrack: Value is not a valid number.",this,o,c),t=!1;break}}return t}optimize(){let t=this.times.slice(),e=this.values.slice(),n=this.getValueSize(),i=this.getInterpolation()===_n,s=t.length-1,r=1;for(let o=1;o<s;++o){let a=!1,c=t[o],l=t[o+1];if(c!==l&&(o!==1||c!==t[0]))if(i)a=!0;else{let f=o*n,u=f-n,d=f+n;for(let p=0;p!==n;++p){let m=e[f+p];if(m!==e[u+p]||m!==e[d+p]){a=!0;break}}}if(a){if(o!==r){t[r]=t[o];let f=o*n,u=r*n;for(let d=0;d!==n;++d)e[u+d]=e[f+d]}++r}}if(s>0){t[r]=t[s];for(let o=s*n,a=r*n,c=0;c!==n;++c)e[a+c]=e[o+c];++r}return r!==t.length?(this.times=t.slice(0,r),this.values=e.slice(0,r*n)):(this.times=t,this.values=e),this}clone(){let t=this.times.slice(),e=this.values.slice(),n=this.constructor,i=new n(this.name,t,e);return i.createInterpolant=this.createInterpolant,i}};ft.prototype.ValueTypeName="";ft.prototype.TimeBufferType=Float32Array;ft.prototype.ValueBufferType=Float32Array;ft.prototype.DefaultInterpolation=yn;var kt=class extends ft{constructor(t,e,n){super(t,e,n)}};kt.prototype.ValueTypeName="bool";kt.prototype.ValueBufferType=Array;kt.prototype.DefaultInterpolation=He;kt.prototype.InterpolantFactoryMethodLinear=void 0;kt.prototype.InterpolantFactoryMethodSmooth=void 0;var In=class extends ft{constructor(t,e,n,i){super(t,e,n,i)}};In.prototype.ValueTypeName="color";var Pn=class extends ft{constructor(t,e,n,i){super(t,e,n,i)}};Pn.prototype.ValueTypeName="number";var Dn=class extends te{constructor(t,e,n,i){super(t,e,n,i)}interpolate_(t,e,n,i){let s=this.resultBuffer,r=this.sampleValues,o=this.valueSize,a=(n-e)/(i-e),c=t*o;for(let l=c+o;c!==l;c+=4)Pt.slerpFlat(s,0,r,c-o,r,c,a);return s}},qe=class extends ft{constructor(t,e,n,i){super(t,e,n,i)}InterpolantFactoryMethodLinear(t){return new Dn(this.times,this.values,this.getValueSize(),t)}};qe.prototype.ValueTypeName="quaternion";qe.prototype.InterpolantFactoryMethodSmooth=void 0;var Ht=class extends ft{constructor(t,e,n){super(t,e,n)}};Ht.prototype.ValueTypeName="string";Ht.prototype.ValueBufferType=Array;Ht.prototype.DefaultInterpolation=He;Ht.prototype.InterpolantFactoryMethodLinear=void 0;Ht.prototype.InterpolantFactoryMethodSmooth=void 0;var Ln=class extends ft{constructor(t,e,n,i){super(t,e,n,i)}};Ln.prototype.ValueTypeName="vector";var Un=class{constructor(t,e,n){let i=this,s=!1,r=0,o=0,a,c=[];this.onStart=void 0,this.onLoad=t,this.onProgress=e,this.onError=n,this.abortController=new AbortController,this.itemStart=function(l){o++,s===!1&&i.onStart!==void 0&&i.onStart(l,r,o),s=!0},this.itemEnd=function(l){r++,i.onProgress!==void 0&&i.onProgress(l,r,o),r===o&&(s=!1,i.onLoad!==void 0&&i.onLoad())},this.itemError=function(l){i.onError!==void 0&&i.onError(l)},this.resolveURL=function(l){return a?a(l):l},this.setURLModifier=function(l){return a=l,this},this.addHandler=function(l,f){return c.push(l,f),this},this.removeHandler=function(l){let f=c.indexOf(l);return f!==-1&&c.splice(f,2),this},this.getHandler=function(l){for(let f=0,u=c.length;f<u;f+=2){let d=c[f],p=c[f+1];if(d.global&&(d.lastIndex=0),d.test(l))return p}return null},this.abort=function(){return this.abortController.abort(),this.abortController=new AbortController,this}}},Ys=new Un,Nn=class{constructor(t){this.manager=t!==void 0?t:Ys,this.crossOrigin="anonymous",this.withCredentials=!1,this.path="",this.resourcePath="",this.requestHeader={}}load(){}loadAsync(t,e){let n=this;return new Promise(function(i,s){n.load(t,i,e,s)})}parse(){}setCrossOrigin(t){return this.crossOrigin=t,this}setWithCredentials(t){return this.withCredentials=t,this}setPath(t){return this.path=t,this}setResourcePath(t){return this.resourcePath=t,this}setRequestHeader(t){return this.requestHeader=t,this}abort(){return this}};Nn.DEFAULT_MATERIAL_NAME="__DEFAULT";var ji="\\[\\]\\.:\\/",oo=new RegExp("["+ji+"]","g"),ts="[^"+ji+"]",ao="[^"+ji.replace("\\.","")+"]",co=/((?:WC+[\/:])*)/.source.replace("WC",ts),lo=/(WCOD+)?/.source.replace("WCOD",ao),uo=/(?:\.(WC+)(?:\[(.+)\])?)?/.source.replace("WC",ts),ho=/\.(WC+)(?:\[(.+)\])?/.source.replace("WC",ts),fo=new RegExp("^"+co+lo+uo+ho+"$"),po=["material","materials","bones","map"],Vi=class{constructor(t,e,n){let i=n||X.parseTrackName(e);this._targetGroup=t,this._bindings=t.subscribe_(e,i)}getValue(t,e){this.bind();let n=this._targetGroup.nCachedObjects_,i=this._bindings[n];i!==void 0&&i.getValue(t,e)}setValue(t,e){let n=this._bindings;for(let i=this._targetGroup.nCachedObjects_,s=n.length;i!==s;++i)n[i].setValue(t,e)}bind(){let t=this._bindings;for(let e=this._targetGroup.nCachedObjects_,n=t.length;e!==n;++e)t[e].bind()}unbind(){let t=this._bindings;for(let e=this._targetGroup.nCachedObjects_,n=t.length;e!==n;++e)t[e].unbind()}},X=class h{constructor(t,e,n){this.path=e,this.parsedPath=n||h.parseTrackName(e),this.node=h.findNode(t,this.parsedPath.nodeName),this.rootNode=t,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}static create(t,e,n){return t&&t.isAnimationObjectGroup?new h.Composite(t,e,n):new h(t,e,n)}static sanitizeNodeName(t){return t.replace(/\s/g,"_").replace(oo,"")}static parseTrackName(t){let e=fo.exec(t);if(e===null)throw new Error("PropertyBinding: Cannot parse trackName: "+t);let n={nodeName:e[2],objectName:e[3],objectIndex:e[4],propertyName:e[5],propertyIndex:e[6]},i=n.nodeName&&n.nodeName.lastIndexOf(".");if(i!==void 0&&i!==-1){let s=n.nodeName.substring(i+1);po.indexOf(s)!==-1&&(n.nodeName=n.nodeName.substring(0,i),n.objectName=s)}if(n.propertyName===null||n.propertyName.length===0)throw new Error("PropertyBinding: can not parse propertyName from trackName: "+t);return n}static findNode(t,e){if(e===void 0||e===""||e==="."||e===-1||e===t.name||e===t.uuid)return t;if(t.skeleton){let n=t.skeleton.getBoneByName(e);if(n!==void 0)return n}if(t.children){let n=function(s){for(let r=0;r<s.length;r++){let o=s[r];if(o.name===e||o.uuid===e)return o;let a=n(o.children);if(a)return a}return null},i=n(t.children);if(i)return i}return null}_getValue_unavailable(){}_setValue_unavailable(){}_getValue_direct(t,e){t[e]=this.targetObject[this.propertyName]}_getValue_array(t,e){let n=this.resolvedProperty;for(let i=0,s=n.length;i!==s;++i)t[e++]=n[i]}_getValue_arrayElement(t,e){t[e]=this.resolvedProperty[this.propertyIndex]}_getValue_toArray(t,e){this.resolvedProperty.toArray(t,e)}_setValue_direct(t,e){this.targetObject[this.propertyName]=t[e]}_setValue_direct_setNeedsUpdate(t,e){this.targetObject[this.propertyName]=t[e],this.targetObject.needsUpdate=!0}_setValue_direct_setMatrixWorldNeedsUpdate(t,e){this.targetObject[this.propertyName]=t[e],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_array(t,e){let n=this.resolvedProperty;for(let i=0,s=n.length;i!==s;++i)n[i]=t[e++]}_setValue_array_setNeedsUpdate(t,e){let n=this.resolvedProperty;for(let i=0,s=n.length;i!==s;++i)n[i]=t[e++];this.targetObject.needsUpdate=!0}_setValue_array_setMatrixWorldNeedsUpdate(t,e){let n=this.resolvedProperty;for(let i=0,s=n.length;i!==s;++i)n[i]=t[e++];this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_arrayElement(t,e){this.resolvedProperty[this.propertyIndex]=t[e]}_setValue_arrayElement_setNeedsUpdate(t,e){this.resolvedProperty[this.propertyIndex]=t[e],this.targetObject.needsUpdate=!0}_setValue_arrayElement_setMatrixWorldNeedsUpdate(t,e){this.resolvedProperty[this.propertyIndex]=t[e],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_fromArray(t,e){this.resolvedProperty.fromArray(t,e)}_setValue_fromArray_setNeedsUpdate(t,e){this.resolvedProperty.fromArray(t,e),this.targetObject.needsUpdate=!0}_setValue_fromArray_setMatrixWorldNeedsUpdate(t,e){this.resolvedProperty.fromArray(t,e),this.targetObject.matrixWorldNeedsUpdate=!0}_getValue_unbound(t,e){this.bind(),this.getValue(t,e)}_setValue_unbound(t,e){this.bind(),this.setValue(t,e)}bind(){let t=this.node,e=this.parsedPath,n=e.objectName,i=e.propertyName,s=e.propertyIndex;if(t||(t=h.findNode(this.rootNode,e.nodeName),this.node=t),this.getValue=this._getValue_unavailable,this.setValue=this._setValue_unavailable,!t){console.warn("THREE.PropertyBinding: No target node found for track: "+this.path+".");return}if(n){let c=e.objectIndex;switch(n){case"materials":if(!t.material){console.error("THREE.PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!t.material.materials){console.error("THREE.PropertyBinding: Can not bind to material.materials as node.material does not have a materials array.",this);return}t=t.material.materials;break;case"bones":if(!t.skeleton){console.error("THREE.PropertyBinding: Can not bind to bones as node does not have a skeleton.",this);return}t=t.skeleton.bones;for(let l=0;l<t.length;l++)if(t[l].name===c){c=l;break}break;case"map":if("map"in t){t=t.map;break}if(!t.material){console.error("THREE.PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!t.material.map){console.error("THREE.PropertyBinding: Can not bind to material.map as node.material does not have a map.",this);return}t=t.material.map;break;default:if(t[n]===void 0){console.error("THREE.PropertyBinding: Can not bind to objectName of node undefined.",this);return}t=t[n]}if(c!==void 0){if(t[c]===void 0){console.error("THREE.PropertyBinding: Trying to bind to objectIndex of objectName, but is undefined.",this,t);return}t=t[c]}}let r=t[i];if(r===void 0){let c=e.nodeName;console.error("THREE.PropertyBinding: Trying to update property for track: "+c+"."+i+" but it wasn't found.",t);return}let o=this.Versioning.None;this.targetObject=t,t.isMaterial===!0?o=this.Versioning.NeedsUpdate:t.isObject3D===!0&&(o=this.Versioning.MatrixWorldNeedsUpdate);let a=this.BindingType.Direct;if(s!==void 0){if(i==="morphTargetInfluences"){if(!t.geometry){console.error("THREE.PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.",this);return}if(!t.geometry.morphAttributes){console.error("THREE.PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.morphAttributes.",this);return}t.morphTargetDictionary[s]!==void 0&&(s=t.morphTargetDictionary[s])}a=this.BindingType.ArrayElement,this.resolvedProperty=r,this.propertyIndex=s}else r.fromArray!==void 0&&r.toArray!==void 0?(a=this.BindingType.HasFromToArray,this.resolvedProperty=r):Array.isArray(r)?(a=this.BindingType.EntireArray,this.resolvedProperty=r):this.propertyName=i;this.getValue=this.GetterByBindingType[a],this.setValue=this.SetterByBindingTypeAndVersioning[a][o]}unbind(){this.node=null,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}};X.Composite=Vi;X.prototype.BindingType={Direct:0,EntireArray:1,ArrayElement:2,HasFromToArray:3};X.prototype.Versioning={None:0,NeedsUpdate:1,MatrixWorldNeedsUpdate:2};X.prototype.GetterByBindingType=[X.prototype._getValue_direct,X.prototype._getValue_array,X.prototype._getValue_arrayElement,X.prototype._getValue_toArray];X.prototype.SetterByBindingTypeAndVersioning=[[X.prototype._setValue_direct,X.prototype._setValue_direct_setNeedsUpdate,X.prototype._setValue_direct_setMatrixWorldNeedsUpdate],[X.prototype._setValue_array,X.prototype._setValue_array_setNeedsUpdate,X.prototype._setValue_array_setMatrixWorldNeedsUpdate],[X.prototype._setValue_arrayElement,X.prototype._setValue_arrayElement_setNeedsUpdate,X.prototype._setValue_arrayElement_setMatrixWorldNeedsUpdate],[X.prototype._setValue_fromArray,X.prototype._setValue_fromArray_setNeedsUpdate,X.prototype._setValue_fromArray_setMatrixWorldNeedsUpdate]];var bl=new Float32Array(1);var Os=new S,gn=new S,ge=new S,_e=new S,Ci=new S,mo=new S,go=new S,rt=class{constructor(t=new S,e=new S){this.start=t,this.end=e}set(t,e){return this.start.copy(t),this.end.copy(e),this}copy(t){return this.start.copy(t.start),this.end.copy(t.end),this}getCenter(t){return t.addVectors(this.start,this.end).multiplyScalar(.5)}delta(t){return t.subVectors(this.end,this.start)}distanceSq(){return this.start.distanceToSquared(this.end)}distance(){return this.start.distanceTo(this.end)}at(t,e){return this.delta(e).multiplyScalar(t).add(this.start)}closestPointToPointParameter(t,e){Os.subVectors(t,this.start),gn.subVectors(this.end,this.start);let n=gn.dot(gn),s=gn.dot(Os)/n;return e&&(s=U(s,0,1)),s}closestPointToPoint(t,e,n){let i=this.closestPointToPointParameter(t,e);return this.delta(n).multiplyScalar(i).add(this.start)}distanceSqToLine3(t,e=mo,n=go){let i=10000000000000001e-32,s,r,o=this.start,a=t.start,c=this.end,l=t.end;ge.subVectors(c,o),_e.subVectors(l,a),Ci.subVectors(o,a);let f=ge.dot(ge),u=_e.dot(_e),d=_e.dot(Ci);if(f<=i&&u<=i)return e.copy(o),n.copy(a),e.sub(n),e.dot(e);if(f<=i)s=0,r=d/u,r=U(r,0,1);else{let p=ge.dot(Ci);if(u<=i)r=0,s=U(-p/f,0,1);else{let m=ge.dot(_e),v=f*u-m*m;v!==0?s=U((m*d-p*u)/v,0,1):s=0,r=(m*s+d)/u,r<0?(r=0,s=U(-p/f,0,1)):r>1&&(r=1,s=U((m-p)/f,0,1))}}return e.copy(o).add(ge.multiplyScalar(s)),n.copy(a).add(_e.multiplyScalar(r)),e.sub(n),e.dot(e)}applyMatrix4(t){return this.start.applyMatrix4(t),this.end.applyMatrix4(t),this}equals(t){return t.start.equals(this.start)&&t.end.equals(this.end)}clone(){return new this.constructor().copy(this)}};typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:"180"}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__="180");var _o=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,xo=`#ifdef USE_ALPHAHASH
	const float ALPHA_HASH_SCALE = 0.05;
	float hash2D( vec2 value ) {
		return fract( 1.0e4 * sin( 17.0 * value.x + 0.1 * value.y ) * ( 0.1 + abs( sin( 13.0 * value.y + value.x ) ) ) );
	}
	float hash3D( vec3 value ) {
		return hash2D( vec2( hash2D( value.xy ), value.z ) );
	}
	float getAlphaHashThreshold( vec3 position ) {
		float maxDeriv = max(
			length( dFdx( position.xyz ) ),
			length( dFdy( position.xyz ) )
		);
		float pixScale = 1.0 / ( ALPHA_HASH_SCALE * maxDeriv );
		vec2 pixScales = vec2(
			exp2( floor( log2( pixScale ) ) ),
			exp2( ceil( log2( pixScale ) ) )
		);
		vec2 alpha = vec2(
			hash3D( floor( pixScales.x * position.xyz ) ),
			hash3D( floor( pixScales.y * position.xyz ) )
		);
		float lerpFactor = fract( log2( pixScale ) );
		float x = ( 1.0 - lerpFactor ) * alpha.x + lerpFactor * alpha.y;
		float a = min( lerpFactor, 1.0 - lerpFactor );
		vec3 cases = vec3(
			x * x / ( 2.0 * a * ( 1.0 - a ) ),
			( x - 0.5 * a ) / ( 1.0 - a ),
			1.0 - ( ( 1.0 - x ) * ( 1.0 - x ) / ( 2.0 * a * ( 1.0 - a ) ) )
		);
		float threshold = ( x < ( 1.0 - a ) )
			? ( ( x < a ) ? cases.x : cases.y )
			: cases.z;
		return clamp( threshold , 1.0e-6, 1.0 );
	}
#endif`,yo=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,vo=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,Mo=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,So=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,bo=`#ifdef USE_AOMAP
	float ambientOcclusion = ( texture2D( aoMap, vAoMapUv ).r - 1.0 ) * aoMapIntensity + 1.0;
	reflectedLight.indirectDiffuse *= ambientOcclusion;
	#if defined( USE_CLEARCOAT ) 
		clearcoatSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_SHEEN ) 
		sheenSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD )
		float dotNV = saturate( dot( geometryNormal, geometryViewDir ) );
		reflectedLight.indirectSpecular *= computeSpecularOcclusion( dotNV, ambientOcclusion, material.roughness );
	#endif
#endif`,To=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,Eo=`#ifdef USE_BATCHING
	#if ! defined( GL_ANGLE_multi_draw )
	#define gl_DrawID _gl_DrawID
	uniform int _gl_DrawID;
	#endif
	uniform highp sampler2D batchingTexture;
	uniform highp usampler2D batchingIdTexture;
	mat4 getBatchingMatrix( const in float i ) {
		int size = textureSize( batchingTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( batchingTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( batchingTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( batchingTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( batchingTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
	float getIndirectIndex( const in int i ) {
		int size = textureSize( batchingIdTexture, 0 ).x;
		int x = i % size;
		int y = i / size;
		return float( texelFetch( batchingIdTexture, ivec2( x, y ), 0 ).r );
	}
#endif
#ifdef USE_BATCHING_COLOR
	uniform sampler2D batchingColorTexture;
	vec3 getBatchingColor( const in float i ) {
		int size = textureSize( batchingColorTexture, 0 ).x;
		int j = int( i );
		int x = j % size;
		int y = j / size;
		return texelFetch( batchingColorTexture, ivec2( x, y ), 0 ).rgb;
	}
#endif`,Ao=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,wo=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,Co=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,Ro=`float G_BlinnPhong_Implicit( ) {
	return 0.25;
}
float D_BlinnPhong( const in float shininess, const in float dotNH ) {
	return RECIPROCAL_PI * ( shininess * 0.5 + 1.0 ) * pow( dotNH, shininess );
}
vec3 BRDF_BlinnPhong( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in vec3 specularColor, const in float shininess ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( specularColor, 1.0, dotVH );
	float G = G_BlinnPhong_Implicit( );
	float D = D_BlinnPhong( shininess, dotNH );
	return F * ( G * D );
} // validated`,Io=`#ifdef USE_IRIDESCENCE
	const mat3 XYZ_TO_REC709 = mat3(
		 3.2404542, -0.9692660,  0.0556434,
		-1.5371385,  1.8760108, -0.2040259,
		-0.4985314,  0.0415560,  1.0572252
	);
	vec3 Fresnel0ToIor( vec3 fresnel0 ) {
		vec3 sqrtF0 = sqrt( fresnel0 );
		return ( vec3( 1.0 ) + sqrtF0 ) / ( vec3( 1.0 ) - sqrtF0 );
	}
	vec3 IorToFresnel0( vec3 transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - vec3( incidentIor ) ) / ( transmittedIor + vec3( incidentIor ) ) );
	}
	float IorToFresnel0( float transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - incidentIor ) / ( transmittedIor + incidentIor ));
	}
	vec3 evalSensitivity( float OPD, vec3 shift ) {
		float phase = 2.0 * PI * OPD * 1.0e-9;
		vec3 val = vec3( 5.4856e-13, 4.4201e-13, 5.2481e-13 );
		vec3 pos = vec3( 1.6810e+06, 1.7953e+06, 2.2084e+06 );
		vec3 var = vec3( 4.3278e+09, 9.3046e+09, 6.6121e+09 );
		vec3 xyz = val * sqrt( 2.0 * PI * var ) * cos( pos * phase + shift ) * exp( - pow2( phase ) * var );
		xyz.x += 9.7470e-14 * sqrt( 2.0 * PI * 4.5282e+09 ) * cos( 2.2399e+06 * phase + shift[ 0 ] ) * exp( - 4.5282e+09 * pow2( phase ) );
		xyz /= 1.0685e-7;
		vec3 rgb = XYZ_TO_REC709 * xyz;
		return rgb;
	}
	vec3 evalIridescence( float outsideIOR, float eta2, float cosTheta1, float thinFilmThickness, vec3 baseF0 ) {
		vec3 I;
		float iridescenceIOR = mix( outsideIOR, eta2, smoothstep( 0.0, 0.03, thinFilmThickness ) );
		float sinTheta2Sq = pow2( outsideIOR / iridescenceIOR ) * ( 1.0 - pow2( cosTheta1 ) );
		float cosTheta2Sq = 1.0 - sinTheta2Sq;
		if ( cosTheta2Sq < 0.0 ) {
			return vec3( 1.0 );
		}
		float cosTheta2 = sqrt( cosTheta2Sq );
		float R0 = IorToFresnel0( iridescenceIOR, outsideIOR );
		float R12 = F_Schlick( R0, 1.0, cosTheta1 );
		float T121 = 1.0 - R12;
		float phi12 = 0.0;
		if ( iridescenceIOR < outsideIOR ) phi12 = PI;
		float phi21 = PI - phi12;
		vec3 baseIOR = Fresnel0ToIor( clamp( baseF0, 0.0, 0.9999 ) );		vec3 R1 = IorToFresnel0( baseIOR, iridescenceIOR );
		vec3 R23 = F_Schlick( R1, 1.0, cosTheta2 );
		vec3 phi23 = vec3( 0.0 );
		if ( baseIOR[ 0 ] < iridescenceIOR ) phi23[ 0 ] = PI;
		if ( baseIOR[ 1 ] < iridescenceIOR ) phi23[ 1 ] = PI;
		if ( baseIOR[ 2 ] < iridescenceIOR ) phi23[ 2 ] = PI;
		float OPD = 2.0 * iridescenceIOR * thinFilmThickness * cosTheta2;
		vec3 phi = vec3( phi21 ) + phi23;
		vec3 R123 = clamp( R12 * R23, 1e-5, 0.9999 );
		vec3 r123 = sqrt( R123 );
		vec3 Rs = pow2( T121 ) * R23 / ( vec3( 1.0 ) - R123 );
		vec3 C0 = R12 + Rs;
		I = C0;
		vec3 Cm = Rs - T121;
		for ( int m = 1; m <= 2; ++ m ) {
			Cm *= r123;
			vec3 Sm = 2.0 * evalSensitivity( float( m ) * OPD, float( m ) * phi );
			I += Cm * Sm;
		}
		return max( I, vec3( 0.0 ) );
	}
#endif`,Po=`#ifdef USE_BUMPMAP
	uniform sampler2D bumpMap;
	uniform float bumpScale;
	vec2 dHdxy_fwd() {
		vec2 dSTdx = dFdx( vBumpMapUv );
		vec2 dSTdy = dFdy( vBumpMapUv );
		float Hll = bumpScale * texture2D( bumpMap, vBumpMapUv ).x;
		float dBx = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdx ).x - Hll;
		float dBy = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdy ).x - Hll;
		return vec2( dBx, dBy );
	}
	vec3 perturbNormalArb( vec3 surf_pos, vec3 surf_norm, vec2 dHdxy, float faceDirection ) {
		vec3 vSigmaX = normalize( dFdx( surf_pos.xyz ) );
		vec3 vSigmaY = normalize( dFdy( surf_pos.xyz ) );
		vec3 vN = surf_norm;
		vec3 R1 = cross( vSigmaY, vN );
		vec3 R2 = cross( vN, vSigmaX );
		float fDet = dot( vSigmaX, R1 ) * faceDirection;
		vec3 vGrad = sign( fDet ) * ( dHdxy.x * R1 + dHdxy.y * R2 );
		return normalize( abs( fDet ) * surf_norm - vGrad );
	}
#endif`,Do=`#if NUM_CLIPPING_PLANES > 0
	vec4 plane;
	#ifdef ALPHA_TO_COVERAGE
		float distanceToPlane, distanceGradient;
		float clipOpacity = 1.0;
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
			distanceGradient = fwidth( distanceToPlane ) / 2.0;
			clipOpacity *= smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			if ( clipOpacity == 0.0 ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			float unionClipOpacity = 1.0;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
				distanceGradient = fwidth( distanceToPlane ) / 2.0;
				unionClipOpacity *= 1.0 - smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			}
			#pragma unroll_loop_end
			clipOpacity *= 1.0 - unionClipOpacity;
		#endif
		diffuseColor.a *= clipOpacity;
		if ( diffuseColor.a == 0.0 ) discard;
	#else
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			if ( dot( vClipPosition, plane.xyz ) > plane.w ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			bool clipped = true;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				clipped = ( dot( vClipPosition, plane.xyz ) > plane.w ) && clipped;
			}
			#pragma unroll_loop_end
			if ( clipped ) discard;
		#endif
	#endif
#endif`,Lo=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,Uo=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,No=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,Fo=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,Bo=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,Oo=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,zo=`#if defined( USE_COLOR_ALPHA )
	vColor = vec4( 1.0 );
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	vColor = vec3( 1.0 );
#endif
#ifdef USE_COLOR
	vColor *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.xyz *= instanceColor.xyz;
#endif
#ifdef USE_BATCHING_COLOR
	vec3 batchingColor = getBatchingColor( getIndirectIndex( gl_DrawID ) );
	vColor.xyz *= batchingColor.xyz;
#endif`,Vo=`#define PI 3.141592653589793
#define PI2 6.283185307179586
#define PI_HALF 1.5707963267948966
#define RECIPROCAL_PI 0.3183098861837907
#define RECIPROCAL_PI2 0.15915494309189535
#define EPSILON 1e-6
#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
#define whiteComplement( a ) ( 1.0 - saturate( a ) )
float pow2( const in float x ) { return x*x; }
vec3 pow2( const in vec3 x ) { return x*x; }
float pow3( const in float x ) { return x*x*x; }
float pow4( const in float x ) { float x2 = x*x; return x2*x2; }
float max3( const in vec3 v ) { return max( max( v.x, v.y ), v.z ); }
float average( const in vec3 v ) { return dot( v, vec3( 0.3333333 ) ); }
highp float rand( const in vec2 uv ) {
	const highp float a = 12.9898, b = 78.233, c = 43758.5453;
	highp float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
	return fract( sin( sn ) * c );
}
#ifdef HIGH_PRECISION
	float precisionSafeLength( vec3 v ) { return length( v ); }
#else
	float precisionSafeLength( vec3 v ) {
		float maxComponent = max3( abs( v ) );
		return length( v / maxComponent ) * maxComponent;
	}
#endif
struct IncidentLight {
	vec3 color;
	vec3 direction;
	bool visible;
};
struct ReflectedLight {
	vec3 directDiffuse;
	vec3 directSpecular;
	vec3 indirectDiffuse;
	vec3 indirectSpecular;
};
#ifdef USE_ALPHAHASH
	varying vec3 vPosition;
#endif
vec3 transformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );
}
vec3 inverseTransformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( vec4( dir, 0.0 ) * matrix ).xyz );
}
mat3 transposeMat3( const in mat3 m ) {
	mat3 tmp;
	tmp[ 0 ] = vec3( m[ 0 ].x, m[ 1 ].x, m[ 2 ].x );
	tmp[ 1 ] = vec3( m[ 0 ].y, m[ 1 ].y, m[ 2 ].y );
	tmp[ 2 ] = vec3( m[ 0 ].z, m[ 1 ].z, m[ 2 ].z );
	return tmp;
}
bool isPerspectiveMatrix( mat4 m ) {
	return m[ 2 ][ 3 ] == - 1.0;
}
vec2 equirectUv( in vec3 dir ) {
	float u = atan( dir.z, dir.x ) * RECIPROCAL_PI2 + 0.5;
	float v = asin( clamp( dir.y, - 1.0, 1.0 ) ) * RECIPROCAL_PI + 0.5;
	return vec2( u, v );
}
vec3 BRDF_Lambert( const in vec3 diffuseColor ) {
	return RECIPROCAL_PI * diffuseColor;
}
vec3 F_Schlick( const in vec3 f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
}
float F_Schlick( const in float f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
} // validated`,ko=`#ifdef ENVMAP_TYPE_CUBE_UV
	#define cubeUV_minMipLevel 4.0
	#define cubeUV_minTileSize 16.0
	float getFace( vec3 direction ) {
		vec3 absDirection = abs( direction );
		float face = - 1.0;
		if ( absDirection.x > absDirection.z ) {
			if ( absDirection.x > absDirection.y )
				face = direction.x > 0.0 ? 0.0 : 3.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		} else {
			if ( absDirection.z > absDirection.y )
				face = direction.z > 0.0 ? 2.0 : 5.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		}
		return face;
	}
	vec2 getUV( vec3 direction, float face ) {
		vec2 uv;
		if ( face == 0.0 ) {
			uv = vec2( direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 1.0 ) {
			uv = vec2( - direction.x, - direction.z ) / abs( direction.y );
		} else if ( face == 2.0 ) {
			uv = vec2( - direction.x, direction.y ) / abs( direction.z );
		} else if ( face == 3.0 ) {
			uv = vec2( - direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 4.0 ) {
			uv = vec2( - direction.x, direction.z ) / abs( direction.y );
		} else {
			uv = vec2( direction.x, direction.y ) / abs( direction.z );
		}
		return 0.5 * ( uv + 1.0 );
	}
	vec3 bilinearCubeUV( sampler2D envMap, vec3 direction, float mipInt ) {
		float face = getFace( direction );
		float filterInt = max( cubeUV_minMipLevel - mipInt, 0.0 );
		mipInt = max( mipInt, cubeUV_minMipLevel );
		float faceSize = exp2( mipInt );
		highp vec2 uv = getUV( direction, face ) * ( faceSize - 2.0 ) + 1.0;
		if ( face > 2.0 ) {
			uv.y += faceSize;
			face -= 3.0;
		}
		uv.x += face * faceSize;
		uv.x += filterInt * 3.0 * cubeUV_minTileSize;
		uv.y += 4.0 * ( exp2( CUBEUV_MAX_MIP ) - faceSize );
		uv.x *= CUBEUV_TEXEL_WIDTH;
		uv.y *= CUBEUV_TEXEL_HEIGHT;
		#ifdef texture2DGradEXT
			return texture2DGradEXT( envMap, uv, vec2( 0.0 ), vec2( 0.0 ) ).rgb;
		#else
			return texture2D( envMap, uv ).rgb;
		#endif
	}
	#define cubeUV_r0 1.0
	#define cubeUV_m0 - 2.0
	#define cubeUV_r1 0.8
	#define cubeUV_m1 - 1.0
	#define cubeUV_r4 0.4
	#define cubeUV_m4 2.0
	#define cubeUV_r5 0.305
	#define cubeUV_m5 3.0
	#define cubeUV_r6 0.21
	#define cubeUV_m6 4.0
	float roughnessToMip( float roughness ) {
		float mip = 0.0;
		if ( roughness >= cubeUV_r1 ) {
			mip = ( cubeUV_r0 - roughness ) * ( cubeUV_m1 - cubeUV_m0 ) / ( cubeUV_r0 - cubeUV_r1 ) + cubeUV_m0;
		} else if ( roughness >= cubeUV_r4 ) {
			mip = ( cubeUV_r1 - roughness ) * ( cubeUV_m4 - cubeUV_m1 ) / ( cubeUV_r1 - cubeUV_r4 ) + cubeUV_m1;
		} else if ( roughness >= cubeUV_r5 ) {
			mip = ( cubeUV_r4 - roughness ) * ( cubeUV_m5 - cubeUV_m4 ) / ( cubeUV_r4 - cubeUV_r5 ) + cubeUV_m4;
		} else if ( roughness >= cubeUV_r6 ) {
			mip = ( cubeUV_r5 - roughness ) * ( cubeUV_m6 - cubeUV_m5 ) / ( cubeUV_r5 - cubeUV_r6 ) + cubeUV_m5;
		} else {
			mip = - 2.0 * log2( 1.16 * roughness );		}
		return mip;
	}
	vec4 textureCubeUV( sampler2D envMap, vec3 sampleDir, float roughness ) {
		float mip = clamp( roughnessToMip( roughness ), cubeUV_m0, CUBEUV_MAX_MIP );
		float mipF = fract( mip );
		float mipInt = floor( mip );
		vec3 color0 = bilinearCubeUV( envMap, sampleDir, mipInt );
		if ( mipF == 0.0 ) {
			return vec4( color0, 1.0 );
		} else {
			vec3 color1 = bilinearCubeUV( envMap, sampleDir, mipInt + 1.0 );
			return vec4( mix( color0, color1, mipF ), 1.0 );
		}
	}
#endif`,Ho=`vec3 transformedNormal = objectNormal;
#ifdef USE_TANGENT
	vec3 transformedTangent = objectTangent;
#endif
#ifdef USE_BATCHING
	mat3 bm = mat3( batchingMatrix );
	transformedNormal /= vec3( dot( bm[ 0 ], bm[ 0 ] ), dot( bm[ 1 ], bm[ 1 ] ), dot( bm[ 2 ], bm[ 2 ] ) );
	transformedNormal = bm * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = bm * transformedTangent;
	#endif
#endif
#ifdef USE_INSTANCING
	mat3 im = mat3( instanceMatrix );
	transformedNormal /= vec3( dot( im[ 0 ], im[ 0 ] ), dot( im[ 1 ], im[ 1 ] ), dot( im[ 2 ], im[ 2 ] ) );
	transformedNormal = im * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = im * transformedTangent;
	#endif
#endif
transformedNormal = normalMatrix * transformedNormal;
#ifdef FLIP_SIDED
	transformedNormal = - transformedNormal;
#endif
#ifdef USE_TANGENT
	transformedTangent = ( modelViewMatrix * vec4( transformedTangent, 0.0 ) ).xyz;
	#ifdef FLIP_SIDED
		transformedTangent = - transformedTangent;
	#endif
#endif`,Go=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,Wo=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,Xo=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,qo=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,Yo="gl_FragColor = linearToOutputTexel( gl_FragColor );",Zo=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,Jo=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vec3 cameraToFrag;
		if ( isOrthographic ) {
			cameraToFrag = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToFrag = normalize( vWorldPosition - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vec3 reflectVec = reflect( cameraToFrag, worldNormal );
		#else
			vec3 reflectVec = refract( cameraToFrag, worldNormal, refractionRatio );
		#endif
	#else
		vec3 reflectVec = vReflect;
	#endif
	#ifdef ENVMAP_TYPE_CUBE
		vec4 envColor = textureCube( envMap, envMapRotation * vec3( flipEnvMap * reflectVec.x, reflectVec.yz ) );
	#else
		vec4 envColor = vec4( 0.0 );
	#endif
	#ifdef ENVMAP_BLENDING_MULTIPLY
		outgoingLight = mix( outgoingLight, outgoingLight * envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_MIX )
		outgoingLight = mix( outgoingLight, envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_ADD )
		outgoingLight += envColor.xyz * specularStrength * reflectivity;
	#endif
#endif`,$o=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,Ko=`#ifdef USE_ENVMAP
	uniform float reflectivity;
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		varying vec3 vWorldPosition;
		uniform float refractionRatio;
	#else
		varying vec3 vReflect;
	#endif
#endif`,Qo=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,jo=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vWorldPosition = worldPosition.xyz;
	#else
		vec3 cameraToVertex;
		if ( isOrthographic ) {
			cameraToVertex = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToVertex = normalize( worldPosition.xyz - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vReflect = reflect( cameraToVertex, worldNormal );
		#else
			vReflect = refract( cameraToVertex, worldNormal, refractionRatio );
		#endif
	#endif
#endif`,ta=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,ea=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,na=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,ia=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,sa=`#ifdef USE_GRADIENTMAP
	uniform sampler2D gradientMap;
#endif
vec3 getGradientIrradiance( vec3 normal, vec3 lightDirection ) {
	float dotNL = dot( normal, lightDirection );
	vec2 coord = vec2( dotNL * 0.5 + 0.5, 0.0 );
	#ifdef USE_GRADIENTMAP
		return vec3( texture2D( gradientMap, coord ).r );
	#else
		vec2 fw = fwidth( coord ) * 0.5;
		return mix( vec3( 0.7 ), vec3( 1.0 ), smoothstep( 0.7 - fw.x, 0.7 + fw.x, coord.x ) );
	#endif
}`,ra=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,oa=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,aa=`varying vec3 vViewPosition;
struct LambertMaterial {
	vec3 diffuseColor;
	float specularStrength;
};
void RE_Direct_Lambert( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Lambert( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Lambert
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,ca=`uniform bool receiveShadow;
uniform vec3 ambientLightColor;
#if defined( USE_LIGHT_PROBES )
	uniform vec3 lightProbe[ 9 ];
#endif
vec3 shGetIrradianceAt( in vec3 normal, in vec3 shCoefficients[ 9 ] ) {
	float x = normal.x, y = normal.y, z = normal.z;
	vec3 result = shCoefficients[ 0 ] * 0.886227;
	result += shCoefficients[ 1 ] * 2.0 * 0.511664 * y;
	result += shCoefficients[ 2 ] * 2.0 * 0.511664 * z;
	result += shCoefficients[ 3 ] * 2.0 * 0.511664 * x;
	result += shCoefficients[ 4 ] * 2.0 * 0.429043 * x * y;
	result += shCoefficients[ 5 ] * 2.0 * 0.429043 * y * z;
	result += shCoefficients[ 6 ] * ( 0.743125 * z * z - 0.247708 );
	result += shCoefficients[ 7 ] * 2.0 * 0.429043 * x * z;
	result += shCoefficients[ 8 ] * 0.429043 * ( x * x - y * y );
	return result;
}
vec3 getLightProbeIrradiance( const in vec3 lightProbe[ 9 ], const in vec3 normal ) {
	vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
	vec3 irradiance = shGetIrradianceAt( worldNormal, lightProbe );
	return irradiance;
}
vec3 getAmbientLightIrradiance( const in vec3 ambientLightColor ) {
	vec3 irradiance = ambientLightColor;
	return irradiance;
}
float getDistanceAttenuation( const in float lightDistance, const in float cutoffDistance, const in float decayExponent ) {
	float distanceFalloff = 1.0 / max( pow( lightDistance, decayExponent ), 0.01 );
	if ( cutoffDistance > 0.0 ) {
		distanceFalloff *= pow2( saturate( 1.0 - pow4( lightDistance / cutoffDistance ) ) );
	}
	return distanceFalloff;
}
float getSpotAttenuation( const in float coneCosine, const in float penumbraCosine, const in float angleCosine ) {
	return smoothstep( coneCosine, penumbraCosine, angleCosine );
}
#if NUM_DIR_LIGHTS > 0
	struct DirectionalLight {
		vec3 direction;
		vec3 color;
	};
	uniform DirectionalLight directionalLights[ NUM_DIR_LIGHTS ];
	void getDirectionalLightInfo( const in DirectionalLight directionalLight, out IncidentLight light ) {
		light.color = directionalLight.color;
		light.direction = directionalLight.direction;
		light.visible = true;
	}
#endif
#if NUM_POINT_LIGHTS > 0
	struct PointLight {
		vec3 position;
		vec3 color;
		float distance;
		float decay;
	};
	uniform PointLight pointLights[ NUM_POINT_LIGHTS ];
	void getPointLightInfo( const in PointLight pointLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = pointLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float lightDistance = length( lVector );
		light.color = pointLight.color;
		light.color *= getDistanceAttenuation( lightDistance, pointLight.distance, pointLight.decay );
		light.visible = ( light.color != vec3( 0.0 ) );
	}
#endif
#if NUM_SPOT_LIGHTS > 0
	struct SpotLight {
		vec3 position;
		vec3 direction;
		vec3 color;
		float distance;
		float decay;
		float coneCos;
		float penumbraCos;
	};
	uniform SpotLight spotLights[ NUM_SPOT_LIGHTS ];
	void getSpotLightInfo( const in SpotLight spotLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = spotLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float angleCos = dot( light.direction, spotLight.direction );
		float spotAttenuation = getSpotAttenuation( spotLight.coneCos, spotLight.penumbraCos, angleCos );
		if ( spotAttenuation > 0.0 ) {
			float lightDistance = length( lVector );
			light.color = spotLight.color * spotAttenuation;
			light.color *= getDistanceAttenuation( lightDistance, spotLight.distance, spotLight.decay );
			light.visible = ( light.color != vec3( 0.0 ) );
		} else {
			light.color = vec3( 0.0 );
			light.visible = false;
		}
	}
#endif
#if NUM_RECT_AREA_LIGHTS > 0
	struct RectAreaLight {
		vec3 color;
		vec3 position;
		vec3 halfWidth;
		vec3 halfHeight;
	};
	uniform sampler2D ltc_1;	uniform sampler2D ltc_2;
	uniform RectAreaLight rectAreaLights[ NUM_RECT_AREA_LIGHTS ];
#endif
#if NUM_HEMI_LIGHTS > 0
	struct HemisphereLight {
		vec3 direction;
		vec3 skyColor;
		vec3 groundColor;
	};
	uniform HemisphereLight hemisphereLights[ NUM_HEMI_LIGHTS ];
	vec3 getHemisphereLightIrradiance( const in HemisphereLight hemiLight, const in vec3 normal ) {
		float dotNL = dot( normal, hemiLight.direction );
		float hemiDiffuseWeight = 0.5 * dotNL + 0.5;
		vec3 irradiance = mix( hemiLight.groundColor, hemiLight.skyColor, hemiDiffuseWeight );
		return irradiance;
	}
#endif`,la=`#ifdef USE_ENVMAP
	vec3 getIBLIrradiance( const in vec3 normal ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * worldNormal, 1.0 );
			return PI * envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	vec3 getIBLRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 reflectVec = reflect( - viewDir, normal );
			reflectVec = normalize( mix( reflectVec, normal, roughness * roughness) );
			reflectVec = inverseTransformDirection( reflectVec, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );
			return envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	#ifdef USE_ANISOTROPY
		vec3 getIBLAnisotropyRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 bentNormal = cross( bitangent, viewDir );
				bentNormal = normalize( cross( bentNormal, bitangent ) );
				bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
				return getIBLRadiance( viewDir, bentNormal, roughness );
			#else
				return vec3( 0.0 );
			#endif
		}
	#endif
#endif`,ua=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,ha=`varying vec3 vViewPosition;
struct ToonMaterial {
	vec3 diffuseColor;
};
void RE_Direct_Toon( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 irradiance = getGradientIrradiance( geometryNormal, directLight.direction ) * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Toon( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Toon
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,fa=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,da=`varying vec3 vViewPosition;
struct BlinnPhongMaterial {
	vec3 diffuseColor;
	vec3 specularColor;
	float specularShininess;
	float specularStrength;
};
void RE_Direct_BlinnPhong( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
	reflectedLight.directSpecular += irradiance * BRDF_BlinnPhong( directLight.direction, geometryViewDir, geometryNormal, material.specularColor, material.specularShininess ) * material.specularStrength;
}
void RE_IndirectDiffuse_BlinnPhong( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_BlinnPhong
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,pa=`PhysicalMaterial material;
material.diffuseColor = diffuseColor.rgb * ( 1.0 - metalnessFactor );
vec3 dxy = max( abs( dFdx( nonPerturbedNormal ) ), abs( dFdy( nonPerturbedNormal ) ) );
float geometryRoughness = max( max( dxy.x, dxy.y ), dxy.z );
material.roughness = max( roughnessFactor, 0.0525 );material.roughness += geometryRoughness;
material.roughness = min( material.roughness, 1.0 );
#ifdef IOR
	material.ior = ior;
	#ifdef USE_SPECULAR
		float specularIntensityFactor = specularIntensity;
		vec3 specularColorFactor = specularColor;
		#ifdef USE_SPECULAR_COLORMAP
			specularColorFactor *= texture2D( specularColorMap, vSpecularColorMapUv ).rgb;
		#endif
		#ifdef USE_SPECULAR_INTENSITYMAP
			specularIntensityFactor *= texture2D( specularIntensityMap, vSpecularIntensityMapUv ).a;
		#endif
		material.specularF90 = mix( specularIntensityFactor, 1.0, metalnessFactor );
	#else
		float specularIntensityFactor = 1.0;
		vec3 specularColorFactor = vec3( 1.0 );
		material.specularF90 = 1.0;
	#endif
	material.specularColor = mix( min( pow2( ( material.ior - 1.0 ) / ( material.ior + 1.0 ) ) * specularColorFactor, vec3( 1.0 ) ) * specularIntensityFactor, diffuseColor.rgb, metalnessFactor );
#else
	material.specularColor = mix( vec3( 0.04 ), diffuseColor.rgb, metalnessFactor );
	material.specularF90 = 1.0;
#endif
#ifdef USE_CLEARCOAT
	material.clearcoat = clearcoat;
	material.clearcoatRoughness = clearcoatRoughness;
	material.clearcoatF0 = vec3( 0.04 );
	material.clearcoatF90 = 1.0;
	#ifdef USE_CLEARCOATMAP
		material.clearcoat *= texture2D( clearcoatMap, vClearcoatMapUv ).x;
	#endif
	#ifdef USE_CLEARCOAT_ROUGHNESSMAP
		material.clearcoatRoughness *= texture2D( clearcoatRoughnessMap, vClearcoatRoughnessMapUv ).y;
	#endif
	material.clearcoat = saturate( material.clearcoat );	material.clearcoatRoughness = max( material.clearcoatRoughness, 0.0525 );
	material.clearcoatRoughness += geometryRoughness;
	material.clearcoatRoughness = min( material.clearcoatRoughness, 1.0 );
#endif
#ifdef USE_DISPERSION
	material.dispersion = dispersion;
#endif
#ifdef USE_IRIDESCENCE
	material.iridescence = iridescence;
	material.iridescenceIOR = iridescenceIOR;
	#ifdef USE_IRIDESCENCEMAP
		material.iridescence *= texture2D( iridescenceMap, vIridescenceMapUv ).r;
	#endif
	#ifdef USE_IRIDESCENCE_THICKNESSMAP
		material.iridescenceThickness = (iridescenceThicknessMaximum - iridescenceThicknessMinimum) * texture2D( iridescenceThicknessMap, vIridescenceThicknessMapUv ).g + iridescenceThicknessMinimum;
	#else
		material.iridescenceThickness = iridescenceThicknessMaximum;
	#endif
#endif
#ifdef USE_SHEEN
	material.sheenColor = sheenColor;
	#ifdef USE_SHEEN_COLORMAP
		material.sheenColor *= texture2D( sheenColorMap, vSheenColorMapUv ).rgb;
	#endif
	material.sheenRoughness = clamp( sheenRoughness, 0.07, 1.0 );
	#ifdef USE_SHEEN_ROUGHNESSMAP
		material.sheenRoughness *= texture2D( sheenRoughnessMap, vSheenRoughnessMapUv ).a;
	#endif
#endif
#ifdef USE_ANISOTROPY
	#ifdef USE_ANISOTROPYMAP
		mat2 anisotropyMat = mat2( anisotropyVector.x, anisotropyVector.y, - anisotropyVector.y, anisotropyVector.x );
		vec3 anisotropyPolar = texture2D( anisotropyMap, vAnisotropyMapUv ).rgb;
		vec2 anisotropyV = anisotropyMat * normalize( 2.0 * anisotropyPolar.rg - vec2( 1.0 ) ) * anisotropyPolar.b;
	#else
		vec2 anisotropyV = anisotropyVector;
	#endif
	material.anisotropy = length( anisotropyV );
	if( material.anisotropy == 0.0 ) {
		anisotropyV = vec2( 1.0, 0.0 );
	} else {
		anisotropyV /= material.anisotropy;
		material.anisotropy = saturate( material.anisotropy );
	}
	material.alphaT = mix( pow2( material.roughness ), 1.0, pow2( material.anisotropy ) );
	material.anisotropyT = tbn[ 0 ] * anisotropyV.x + tbn[ 1 ] * anisotropyV.y;
	material.anisotropyB = tbn[ 1 ] * anisotropyV.x - tbn[ 0 ] * anisotropyV.y;
#endif`,ma=`struct PhysicalMaterial {
	vec3 diffuseColor;
	float roughness;
	vec3 specularColor;
	float specularF90;
	float dispersion;
	#ifdef USE_CLEARCOAT
		float clearcoat;
		float clearcoatRoughness;
		vec3 clearcoatF0;
		float clearcoatF90;
	#endif
	#ifdef USE_IRIDESCENCE
		float iridescence;
		float iridescenceIOR;
		float iridescenceThickness;
		vec3 iridescenceFresnel;
		vec3 iridescenceF0;
	#endif
	#ifdef USE_SHEEN
		vec3 sheenColor;
		float sheenRoughness;
	#endif
	#ifdef IOR
		float ior;
	#endif
	#ifdef USE_TRANSMISSION
		float transmission;
		float transmissionAlpha;
		float thickness;
		float attenuationDistance;
		vec3 attenuationColor;
	#endif
	#ifdef USE_ANISOTROPY
		float anisotropy;
		float alphaT;
		vec3 anisotropyT;
		vec3 anisotropyB;
	#endif
};
vec3 clearcoatSpecularDirect = vec3( 0.0 );
vec3 clearcoatSpecularIndirect = vec3( 0.0 );
vec3 sheenSpecularDirect = vec3( 0.0 );
vec3 sheenSpecularIndirect = vec3(0.0 );
vec3 Schlick_to_F0( const in vec3 f, const in float f90, const in float dotVH ) {
    float x = clamp( 1.0 - dotVH, 0.0, 1.0 );
    float x2 = x * x;
    float x5 = clamp( x * x2 * x2, 0.0, 0.9999 );
    return ( f - vec3( f90 ) * x5 ) / ( 1.0 - x5 );
}
float V_GGX_SmithCorrelated( const in float alpha, const in float dotNL, const in float dotNV ) {
	float a2 = pow2( alpha );
	float gv = dotNL * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNV ) );
	float gl = dotNV * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNL ) );
	return 0.5 / max( gv + gl, EPSILON );
}
float D_GGX( const in float alpha, const in float dotNH ) {
	float a2 = pow2( alpha );
	float denom = pow2( dotNH ) * ( a2 - 1.0 ) + 1.0;
	return RECIPROCAL_PI * a2 / pow2( denom );
}
#ifdef USE_ANISOTROPY
	float V_GGX_SmithCorrelated_Anisotropic( const in float alphaT, const in float alphaB, const in float dotTV, const in float dotBV, const in float dotTL, const in float dotBL, const in float dotNV, const in float dotNL ) {
		float gv = dotNL * length( vec3( alphaT * dotTV, alphaB * dotBV, dotNV ) );
		float gl = dotNV * length( vec3( alphaT * dotTL, alphaB * dotBL, dotNL ) );
		float v = 0.5 / ( gv + gl );
		return saturate(v);
	}
	float D_GGX_Anisotropic( const in float alphaT, const in float alphaB, const in float dotNH, const in float dotTH, const in float dotBH ) {
		float a2 = alphaT * alphaB;
		highp vec3 v = vec3( alphaB * dotTH, alphaT * dotBH, a2 * dotNH );
		highp float v2 = dot( v, v );
		float w2 = a2 / v2;
		return RECIPROCAL_PI * a2 * pow2 ( w2 );
	}
#endif
#ifdef USE_CLEARCOAT
	vec3 BRDF_GGX_Clearcoat( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material) {
		vec3 f0 = material.clearcoatF0;
		float f90 = material.clearcoatF90;
		float roughness = material.clearcoatRoughness;
		float alpha = pow2( roughness );
		vec3 halfDir = normalize( lightDir + viewDir );
		float dotNL = saturate( dot( normal, lightDir ) );
		float dotNV = saturate( dot( normal, viewDir ) );
		float dotNH = saturate( dot( normal, halfDir ) );
		float dotVH = saturate( dot( viewDir, halfDir ) );
		vec3 F = F_Schlick( f0, f90, dotVH );
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
		return F * ( V * D );
	}
#endif
vec3 BRDF_GGX( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 f0 = material.specularColor;
	float f90 = material.specularF90;
	float roughness = material.roughness;
	float alpha = pow2( roughness );
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( f0, f90, dotVH );
	#ifdef USE_IRIDESCENCE
		F = mix( F, material.iridescenceFresnel, material.iridescence );
	#endif
	#ifdef USE_ANISOTROPY
		float dotTL = dot( material.anisotropyT, lightDir );
		float dotTV = dot( material.anisotropyT, viewDir );
		float dotTH = dot( material.anisotropyT, halfDir );
		float dotBL = dot( material.anisotropyB, lightDir );
		float dotBV = dot( material.anisotropyB, viewDir );
		float dotBH = dot( material.anisotropyB, halfDir );
		float V = V_GGX_SmithCorrelated_Anisotropic( material.alphaT, alpha, dotTV, dotBV, dotTL, dotBL, dotNV, dotNL );
		float D = D_GGX_Anisotropic( material.alphaT, alpha, dotNH, dotTH, dotBH );
	#else
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
	#endif
	return F * ( V * D );
}
vec2 LTC_Uv( const in vec3 N, const in vec3 V, const in float roughness ) {
	const float LUT_SIZE = 64.0;
	const float LUT_SCALE = ( LUT_SIZE - 1.0 ) / LUT_SIZE;
	const float LUT_BIAS = 0.5 / LUT_SIZE;
	float dotNV = saturate( dot( N, V ) );
	vec2 uv = vec2( roughness, sqrt( 1.0 - dotNV ) );
	uv = uv * LUT_SCALE + LUT_BIAS;
	return uv;
}
float LTC_ClippedSphereFormFactor( const in vec3 f ) {
	float l = length( f );
	return max( ( l * l + f.z ) / ( l + 1.0 ), 0.0 );
}
vec3 LTC_EdgeVectorFormFactor( const in vec3 v1, const in vec3 v2 ) {
	float x = dot( v1, v2 );
	float y = abs( x );
	float a = 0.8543985 + ( 0.4965155 + 0.0145206 * y ) * y;
	float b = 3.4175940 + ( 4.1616724 + y ) * y;
	float v = a / b;
	float theta_sintheta = ( x > 0.0 ) ? v : 0.5 * inversesqrt( max( 1.0 - x * x, 1e-7 ) ) - v;
	return cross( v1, v2 ) * theta_sintheta;
}
vec3 LTC_Evaluate( const in vec3 N, const in vec3 V, const in vec3 P, const in mat3 mInv, const in vec3 rectCoords[ 4 ] ) {
	vec3 v1 = rectCoords[ 1 ] - rectCoords[ 0 ];
	vec3 v2 = rectCoords[ 3 ] - rectCoords[ 0 ];
	vec3 lightNormal = cross( v1, v2 );
	if( dot( lightNormal, P - rectCoords[ 0 ] ) < 0.0 ) return vec3( 0.0 );
	vec3 T1, T2;
	T1 = normalize( V - N * dot( V, N ) );
	T2 = - cross( N, T1 );
	mat3 mat = mInv * transposeMat3( mat3( T1, T2, N ) );
	vec3 coords[ 4 ];
	coords[ 0 ] = mat * ( rectCoords[ 0 ] - P );
	coords[ 1 ] = mat * ( rectCoords[ 1 ] - P );
	coords[ 2 ] = mat * ( rectCoords[ 2 ] - P );
	coords[ 3 ] = mat * ( rectCoords[ 3 ] - P );
	coords[ 0 ] = normalize( coords[ 0 ] );
	coords[ 1 ] = normalize( coords[ 1 ] );
	coords[ 2 ] = normalize( coords[ 2 ] );
	coords[ 3 ] = normalize( coords[ 3 ] );
	vec3 vectorFormFactor = vec3( 0.0 );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 0 ], coords[ 1 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 1 ], coords[ 2 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 2 ], coords[ 3 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 3 ], coords[ 0 ] );
	float result = LTC_ClippedSphereFormFactor( vectorFormFactor );
	return vec3( result );
}
#if defined( USE_SHEEN )
float D_Charlie( float roughness, float dotNH ) {
	float alpha = pow2( roughness );
	float invAlpha = 1.0 / alpha;
	float cos2h = dotNH * dotNH;
	float sin2h = max( 1.0 - cos2h, 0.0078125 );
	return ( 2.0 + invAlpha ) * pow( sin2h, invAlpha * 0.5 ) / ( 2.0 * PI );
}
float V_Neubelt( float dotNV, float dotNL ) {
	return saturate( 1.0 / ( 4.0 * ( dotNL + dotNV - dotNL * dotNV ) ) );
}
vec3 BRDF_Sheen( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, vec3 sheenColor, const in float sheenRoughness ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float D = D_Charlie( sheenRoughness, dotNH );
	float V = V_Neubelt( dotNV, dotNL );
	return sheenColor * ( D * V );
}
#endif
float IBLSheenBRDF( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	float r2 = roughness * roughness;
	float a = roughness < 0.25 ? -339.2 * r2 + 161.4 * roughness - 25.9 : -8.48 * r2 + 14.3 * roughness - 9.95;
	float b = roughness < 0.25 ? 44.0 * r2 - 23.7 * roughness + 3.26 : 1.97 * r2 - 3.27 * roughness + 0.72;
	float DG = exp( a * dotNV + b ) + ( roughness < 0.25 ? 0.0 : 0.1 * ( roughness - 0.25 ) );
	return saturate( DG * RECIPROCAL_PI );
}
vec2 DFGApprox( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	const vec4 c0 = vec4( - 1, - 0.0275, - 0.572, 0.022 );
	const vec4 c1 = vec4( 1, 0.0425, 1.04, - 0.04 );
	vec4 r = roughness * c0 + c1;
	float a004 = min( r.x * r.x, exp2( - 9.28 * dotNV ) ) * r.x + r.y;
	vec2 fab = vec2( - 1.04, 1.04 ) * a004 + r.zw;
	return fab;
}
vec3 EnvironmentBRDF( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness ) {
	vec2 fab = DFGApprox( normal, viewDir, roughness );
	return specularColor * fab.x + specularF90 * fab.y;
}
#ifdef USE_IRIDESCENCE
void computeMultiscatteringIridescence( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float iridescence, const in vec3 iridescenceF0, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#else
void computeMultiscattering( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#endif
	vec2 fab = DFGApprox( normal, viewDir, roughness );
	#ifdef USE_IRIDESCENCE
		vec3 Fr = mix( specularColor, iridescenceF0, iridescence );
	#else
		vec3 Fr = specularColor;
	#endif
	vec3 FssEss = Fr * fab.x + specularF90 * fab.y;
	float Ess = fab.x + fab.y;
	float Ems = 1.0 - Ess;
	vec3 Favg = Fr + ( 1.0 - Fr ) * 0.047619;	vec3 Fms = FssEss * Favg / ( 1.0 - Ems * Favg );
	singleScatter += FssEss;
	multiScatter += Fms * Ems;
}
#if NUM_RECT_AREA_LIGHTS > 0
	void RE_Direct_RectArea_Physical( const in RectAreaLight rectAreaLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
		vec3 normal = geometryNormal;
		vec3 viewDir = geometryViewDir;
		vec3 position = geometryPosition;
		vec3 lightPos = rectAreaLight.position;
		vec3 halfWidth = rectAreaLight.halfWidth;
		vec3 halfHeight = rectAreaLight.halfHeight;
		vec3 lightColor = rectAreaLight.color;
		float roughness = material.roughness;
		vec3 rectCoords[ 4 ];
		rectCoords[ 0 ] = lightPos + halfWidth - halfHeight;		rectCoords[ 1 ] = lightPos - halfWidth - halfHeight;
		rectCoords[ 2 ] = lightPos - halfWidth + halfHeight;
		rectCoords[ 3 ] = lightPos + halfWidth + halfHeight;
		vec2 uv = LTC_Uv( normal, viewDir, roughness );
		vec4 t1 = texture2D( ltc_1, uv );
		vec4 t2 = texture2D( ltc_2, uv );
		mat3 mInv = mat3(
			vec3( t1.x, 0, t1.y ),
			vec3(    0, 1,    0 ),
			vec3( t1.z, 0, t1.w )
		);
		vec3 fresnel = ( material.specularColor * t2.x + ( vec3( 1.0 ) - material.specularColor ) * t2.y );
		reflectedLight.directSpecular += lightColor * fresnel * LTC_Evaluate( normal, viewDir, position, mInv, rectCoords );
		reflectedLight.directDiffuse += lightColor * material.diffuseColor * LTC_Evaluate( normal, viewDir, position, mat3( 1.0 ), rectCoords );
	}
#endif
void RE_Direct_Physical( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	#ifdef USE_CLEARCOAT
		float dotNLcc = saturate( dot( geometryClearcoatNormal, directLight.direction ) );
		vec3 ccIrradiance = dotNLcc * directLight.color;
		clearcoatSpecularDirect += ccIrradiance * BRDF_GGX_Clearcoat( directLight.direction, geometryViewDir, geometryClearcoatNormal, material );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularDirect += irradiance * BRDF_Sheen( directLight.direction, geometryViewDir, geometryNormal, material.sheenColor, material.sheenRoughness );
	#endif
	reflectedLight.directSpecular += irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Physical( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectSpecular_Physical( const in vec3 radiance, const in vec3 irradiance, const in vec3 clearcoatRadiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight) {
	#ifdef USE_CLEARCOAT
		clearcoatSpecularIndirect += clearcoatRadiance * EnvironmentBRDF( geometryClearcoatNormal, geometryViewDir, material.clearcoatF0, material.clearcoatF90, material.clearcoatRoughness );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularIndirect += irradiance * material.sheenColor * IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
	#endif
	vec3 singleScattering = vec3( 0.0 );
	vec3 multiScattering = vec3( 0.0 );
	vec3 cosineWeightedIrradiance = irradiance * RECIPROCAL_PI;
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.iridescence, material.iridescenceFresnel, material.roughness, singleScattering, multiScattering );
	#else
		computeMultiscattering( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.roughness, singleScattering, multiScattering );
	#endif
	vec3 totalScattering = singleScattering + multiScattering;
	vec3 diffuse = material.diffuseColor * ( 1.0 - max( max( totalScattering.r, totalScattering.g ), totalScattering.b ) );
	reflectedLight.indirectSpecular += radiance * singleScattering;
	reflectedLight.indirectSpecular += multiScattering * cosineWeightedIrradiance;
	reflectedLight.indirectDiffuse += diffuse * cosineWeightedIrradiance;
}
#define RE_Direct				RE_Direct_Physical
#define RE_Direct_RectArea		RE_Direct_RectArea_Physical
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Physical
#define RE_IndirectSpecular		RE_IndirectSpecular_Physical
float computeSpecularOcclusion( const in float dotNV, const in float ambientOcclusion, const in float roughness ) {
	return saturate( pow( dotNV + ambientOcclusion, exp2( - 16.0 * roughness - 1.0 ) ) - 1.0 + ambientOcclusion );
}`,ga=`
vec3 geometryPosition = - vViewPosition;
vec3 geometryNormal = normal;
vec3 geometryViewDir = ( isOrthographic ) ? vec3( 0, 0, 1 ) : normalize( vViewPosition );
vec3 geometryClearcoatNormal = vec3( 0.0 );
#ifdef USE_CLEARCOAT
	geometryClearcoatNormal = clearcoatNormal;
#endif
#ifdef USE_IRIDESCENCE
	float dotNVi = saturate( dot( normal, geometryViewDir ) );
	if ( material.iridescenceThickness == 0.0 ) {
		material.iridescence = 0.0;
	} else {
		material.iridescence = saturate( material.iridescence );
	}
	if ( material.iridescence > 0.0 ) {
		material.iridescenceFresnel = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.specularColor );
		material.iridescenceF0 = Schlick_to_F0( material.iridescenceFresnel, 1.0, dotNVi );
	}
#endif
IncidentLight directLight;
#if ( NUM_POINT_LIGHTS > 0 ) && defined( RE_Direct )
	PointLight pointLight;
	#if defined( USE_SHADOWMAP ) && NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHTS; i ++ ) {
		pointLight = pointLights[ i ];
		getPointLightInfo( pointLight, geometryPosition, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_POINT_LIGHT_SHADOWS )
		pointLightShadow = pointLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getPointShadow( pointShadowMap[ i ], pointLightShadow.shadowMapSize, pointLightShadow.shadowIntensity, pointLightShadow.shadowBias, pointLightShadow.shadowRadius, vPointShadowCoord[ i ], pointLightShadow.shadowCameraNear, pointLightShadow.shadowCameraFar ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SPOT_LIGHTS > 0 ) && defined( RE_Direct )
	SpotLight spotLight;
	vec4 spotColor;
	vec3 spotLightCoord;
	bool inSpotLightMap;
	#if defined( USE_SHADOWMAP ) && NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHTS; i ++ ) {
		spotLight = spotLights[ i ];
		getSpotLightInfo( spotLight, geometryPosition, directLight );
		#if ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#define SPOT_LIGHT_MAP_INDEX UNROLLED_LOOP_INDEX
		#elif ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		#define SPOT_LIGHT_MAP_INDEX NUM_SPOT_LIGHT_MAPS
		#else
		#define SPOT_LIGHT_MAP_INDEX ( UNROLLED_LOOP_INDEX - NUM_SPOT_LIGHT_SHADOWS + NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#endif
		#if ( SPOT_LIGHT_MAP_INDEX < NUM_SPOT_LIGHT_MAPS )
			spotLightCoord = vSpotLightCoord[ i ].xyz / vSpotLightCoord[ i ].w;
			inSpotLightMap = all( lessThan( abs( spotLightCoord * 2. - 1. ), vec3( 1.0 ) ) );
			spotColor = texture2D( spotLightMap[ SPOT_LIGHT_MAP_INDEX ], spotLightCoord.xy );
			directLight.color = inSpotLightMap ? directLight.color * spotColor.rgb : directLight.color;
		#endif
		#undef SPOT_LIGHT_MAP_INDEX
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		spotLightShadow = spotLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( spotShadowMap[ i ], spotLightShadow.shadowMapSize, spotLightShadow.shadowIntensity, spotLightShadow.shadowBias, spotLightShadow.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_DIR_LIGHTS > 0 ) && defined( RE_Direct )
	DirectionalLight directionalLight;
	#if defined( USE_SHADOWMAP ) && NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHTS; i ++ ) {
		directionalLight = directionalLights[ i ];
		getDirectionalLightInfo( directionalLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_DIR_LIGHT_SHADOWS )
		directionalLightShadow = directionalLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowIntensity, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_RECT_AREA_LIGHTS > 0 ) && defined( RE_Direct_RectArea )
	RectAreaLight rectAreaLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_RECT_AREA_LIGHTS; i ++ ) {
		rectAreaLight = rectAreaLights[ i ];
		RE_Direct_RectArea( rectAreaLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if defined( RE_IndirectDiffuse )
	vec3 iblIrradiance = vec3( 0.0 );
	vec3 irradiance = getAmbientLightIrradiance( ambientLightColor );
	#if defined( USE_LIGHT_PROBES )
		irradiance += getLightProbeIrradiance( lightProbe, geometryNormal );
	#endif
	#if ( NUM_HEMI_LIGHTS > 0 )
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_HEMI_LIGHTS; i ++ ) {
			irradiance += getHemisphereLightIrradiance( hemisphereLights[ i ], geometryNormal );
		}
		#pragma unroll_loop_end
	#endif
#endif
#if defined( RE_IndirectSpecular )
	vec3 radiance = vec3( 0.0 );
	vec3 clearcoatRadiance = vec3( 0.0 );
#endif`,_a=`#if defined( RE_IndirectDiffuse )
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
		irradiance += lightMapIrradiance;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD ) && defined( ENVMAP_TYPE_CUBE_UV )
		iblIrradiance += getIBLIrradiance( geometryNormal );
	#endif
#endif
#if defined( USE_ENVMAP ) && defined( RE_IndirectSpecular )
	#ifdef USE_ANISOTROPY
		radiance += getIBLAnisotropyRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
	#else
		radiance += getIBLRadiance( geometryViewDir, geometryNormal, material.roughness );
	#endif
	#ifdef USE_CLEARCOAT
		clearcoatRadiance += getIBLRadiance( geometryViewDir, geometryClearcoatNormal, material.clearcoatRoughness );
	#endif
#endif`,xa=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,ya=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,va=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Ma=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Sa=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,ba=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,Ta=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,Ea=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
	#if defined( USE_POINTS_UV )
		vec2 uv = vUv;
	#else
		vec2 uv = ( uvTransform * vec3( gl_PointCoord.x, 1.0 - gl_PointCoord.y, 1 ) ).xy;
	#endif
#endif
#ifdef USE_MAP
	diffuseColor *= texture2D( map, uv );
#endif
#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, uv ).g;
#endif`,Aa=`#if defined( USE_POINTS_UV )
	varying vec2 vUv;
#else
	#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
		uniform mat3 uvTransform;
	#endif
#endif
#ifdef USE_MAP
	uniform sampler2D map;
#endif
#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,wa=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,Ca=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,Ra=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,Ia=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,Pa=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Da=`#ifdef USE_MORPHTARGETS
	#ifndef USE_INSTANCING_MORPH
		uniform float morphTargetBaseInfluence;
		uniform float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	#endif
	uniform sampler2DArray morphTargetsTexture;
	uniform ivec2 morphTargetsTextureSize;
	vec4 getMorph( const in int vertexIndex, const in int morphTargetIndex, const in int offset ) {
		int texelIndex = vertexIndex * MORPHTARGETS_TEXTURE_STRIDE + offset;
		int y = texelIndex / morphTargetsTextureSize.x;
		int x = texelIndex - y * morphTargetsTextureSize.x;
		ivec3 morphUV = ivec3( x, y, morphTargetIndex );
		return texelFetch( morphTargetsTexture, morphUV, 0 );
	}
#endif`,La=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Ua=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
#ifdef FLAT_SHADED
	vec3 fdx = dFdx( vViewPosition );
	vec3 fdy = dFdy( vViewPosition );
	vec3 normal = normalize( cross( fdx, fdy ) );
#else
	vec3 normal = normalize( vNormal );
	#ifdef DOUBLE_SIDED
		normal *= faceDirection;
	#endif
#endif
#if defined( USE_NORMALMAP_TANGENTSPACE ) || defined( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY )
	#ifdef USE_TANGENT
		mat3 tbn = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn = getTangentFrame( - vViewPosition, normal,
		#if defined( USE_NORMALMAP )
			vNormalMapUv
		#elif defined( USE_CLEARCOAT_NORMALMAP )
			vClearcoatNormalMapUv
		#else
			vUv
		#endif
		);
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn[0] *= faceDirection;
		tbn[1] *= faceDirection;
	#endif
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	#ifdef USE_TANGENT
		mat3 tbn2 = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn2 = getTangentFrame( - vViewPosition, normal, vClearcoatNormalMapUv );
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn2[0] *= faceDirection;
		tbn2[1] *= faceDirection;
	#endif
#endif
vec3 nonPerturbedNormal = normal;`,Na=`#ifdef USE_NORMALMAP_OBJECTSPACE
	normal = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#ifdef FLIP_SIDED
		normal = - normal;
	#endif
	#ifdef DOUBLE_SIDED
		normal = normal * faceDirection;
	#endif
	normal = normalize( normalMatrix * normal );
#elif defined( USE_NORMALMAP_TANGENTSPACE )
	vec3 mapN = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	mapN.xy *= normalScale;
	normal = normalize( tbn * mapN );
#elif defined( USE_BUMPMAP )
	normal = perturbNormalArb( - vViewPosition, normal, dHdxy_fwd(), faceDirection );
#endif`,Fa=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Ba=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Oa=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,za=`#ifdef USE_NORMALMAP
	uniform sampler2D normalMap;
	uniform vec2 normalScale;
#endif
#ifdef USE_NORMALMAP_OBJECTSPACE
	uniform mat3 normalMatrix;
#endif
#if ! defined ( USE_TANGENT ) && ( defined ( USE_NORMALMAP_TANGENTSPACE ) || defined ( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY ) )
	mat3 getTangentFrame( vec3 eye_pos, vec3 surf_norm, vec2 uv ) {
		vec3 q0 = dFdx( eye_pos.xyz );
		vec3 q1 = dFdy( eye_pos.xyz );
		vec2 st0 = dFdx( uv.st );
		vec2 st1 = dFdy( uv.st );
		vec3 N = surf_norm;
		vec3 q1perp = cross( q1, N );
		vec3 q0perp = cross( N, q0 );
		vec3 T = q1perp * st0.x + q0perp * st1.x;
		vec3 B = q1perp * st0.y + q0perp * st1.y;
		float det = max( dot( T, T ), dot( B, B ) );
		float scale = ( det == 0.0 ) ? 0.0 : inversesqrt( det );
		return mat3( T * scale, B * scale, N );
	}
#endif`,Va=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,ka=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,Ha=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,Ga=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,Wa=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,Xa=`vec3 packNormalToRGB( const in vec3 normal ) {
	return normalize( normal ) * 0.5 + 0.5;
}
vec3 unpackRGBToNormal( const in vec3 rgb ) {
	return 2.0 * rgb.xyz - 1.0;
}
const float PackUpscale = 256. / 255.;const float UnpackDownscale = 255. / 256.;const float ShiftRight8 = 1. / 256.;
const float Inv255 = 1. / 255.;
const vec4 PackFactors = vec4( 1.0, 256.0, 256.0 * 256.0, 256.0 * 256.0 * 256.0 );
const vec2 UnpackFactors2 = vec2( UnpackDownscale, 1.0 / PackFactors.g );
const vec3 UnpackFactors3 = vec3( UnpackDownscale / PackFactors.rg, 1.0 / PackFactors.b );
const vec4 UnpackFactors4 = vec4( UnpackDownscale / PackFactors.rgb, 1.0 / PackFactors.a );
vec4 packDepthToRGBA( const in float v ) {
	if( v <= 0.0 )
		return vec4( 0., 0., 0., 0. );
	if( v >= 1.0 )
		return vec4( 1., 1., 1., 1. );
	float vuf;
	float af = modf( v * PackFactors.a, vuf );
	float bf = modf( vuf * ShiftRight8, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec4( vuf * Inv255, gf * PackUpscale, bf * PackUpscale, af );
}
vec3 packDepthToRGB( const in float v ) {
	if( v <= 0.0 )
		return vec3( 0., 0., 0. );
	if( v >= 1.0 )
		return vec3( 1., 1., 1. );
	float vuf;
	float bf = modf( v * PackFactors.b, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec3( vuf * Inv255, gf * PackUpscale, bf );
}
vec2 packDepthToRG( const in float v ) {
	if( v <= 0.0 )
		return vec2( 0., 0. );
	if( v >= 1.0 )
		return vec2( 1., 1. );
	float vuf;
	float gf = modf( v * 256., vuf );
	return vec2( vuf * Inv255, gf );
}
float unpackRGBAToDepth( const in vec4 v ) {
	return dot( v, UnpackFactors4 );
}
float unpackRGBToDepth( const in vec3 v ) {
	return dot( v, UnpackFactors3 );
}
float unpackRGToDepth( const in vec2 v ) {
	return v.r * UnpackFactors2.r + v.g * UnpackFactors2.g;
}
vec4 pack2HalfToRGBA( const in vec2 v ) {
	vec4 r = vec4( v.x, fract( v.x * 255.0 ), v.y, fract( v.y * 255.0 ) );
	return vec4( r.x - r.y / 255.0, r.y, r.z - r.w / 255.0, r.w );
}
vec2 unpackRGBATo2Half( const in vec4 v ) {
	return vec2( v.x + ( v.y / 255.0 ), v.z + ( v.w / 255.0 ) );
}
float viewZToOrthographicDepth( const in float viewZ, const in float near, const in float far ) {
	return ( viewZ + near ) / ( near - far );
}
float orthographicDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return depth * ( near - far ) - near;
}
float viewZToPerspectiveDepth( const in float viewZ, const in float near, const in float far ) {
	return ( ( near + viewZ ) * far ) / ( ( far - near ) * viewZ );
}
float perspectiveDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return ( near * far ) / ( ( far - near ) * depth - far );
}`,qa=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,Ya=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,Za=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,Ja=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,$a=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,Ka=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,Qa=`#if NUM_SPOT_LIGHT_COORDS > 0
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#if NUM_SPOT_LIGHT_MAPS > 0
	uniform sampler2D spotLightMap[ NUM_SPOT_LIGHT_MAPS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform sampler2D directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		uniform sampler2D spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform sampler2D pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
	float texture2DCompare( sampler2D depths, vec2 uv, float compare ) {
		float depth = unpackRGBAToDepth( texture2D( depths, uv ) );
		#ifdef USE_REVERSED_DEPTH_BUFFER
			return step( depth, compare );
		#else
			return step( compare, depth );
		#endif
	}
	vec2 texture2DDistribution( sampler2D shadow, vec2 uv ) {
		return unpackRGBATo2Half( texture2D( shadow, uv ) );
	}
	float VSMShadow( sampler2D shadow, vec2 uv, float compare ) {
		float occlusion = 1.0;
		vec2 distribution = texture2DDistribution( shadow, uv );
		#ifdef USE_REVERSED_DEPTH_BUFFER
			float hard_shadow = step( distribution.x, compare );
		#else
			float hard_shadow = step( compare, distribution.x );
		#endif
		if ( hard_shadow != 1.0 ) {
			float distance = compare - distribution.x;
			float variance = max( 0.00000, distribution.y * distribution.y );
			float softness_probability = variance / (variance + distance * distance );			softness_probability = clamp( ( softness_probability - 0.3 ) / ( 0.95 - 0.3 ), 0.0, 1.0 );			occlusion = clamp( max( hard_shadow, softness_probability ), 0.0, 1.0 );
		}
		return occlusion;
	}
	float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
		float shadow = 1.0;
		shadowCoord.xyz /= shadowCoord.w;
		shadowCoord.z += shadowBias;
		bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
		bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
		if ( frustumTest ) {
		#if defined( SHADOWMAP_TYPE_PCF )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx0 = - texelSize.x * shadowRadius;
			float dy0 = - texelSize.y * shadowRadius;
			float dx1 = + texelSize.x * shadowRadius;
			float dy1 = + texelSize.y * shadowRadius;
			float dx2 = dx0 / 2.0;
			float dy2 = dy0 / 2.0;
			float dx3 = dx1 / 2.0;
			float dy3 = dy1 / 2.0;
			shadow = (
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy1 ), shadowCoord.z )
			) * ( 1.0 / 17.0 );
		#elif defined( SHADOWMAP_TYPE_PCF_SOFT )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx = texelSize.x;
			float dy = texelSize.y;
			vec2 uv = shadowCoord.xy;
			vec2 f = fract( uv * shadowMapSize + 0.5 );
			uv -= f * texelSize;
			shadow = (
				texture2DCompare( shadowMap, uv, shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( dx, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( 0.0, dy ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + texelSize, shadowCoord.z ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, 0.0 ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 0.0 ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, dy ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( 0.0, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 0.0, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( texture2DCompare( shadowMap, uv + vec2( dx, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( dx, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( mix( texture2DCompare( shadowMap, uv + vec2( -dx, -dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, -dy ), shadowCoord.z ),
						  f.x ),
					 mix( texture2DCompare( shadowMap, uv + vec2( -dx, 2.0 * dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 2.0 * dy ), shadowCoord.z ),
						  f.x ),
					 f.y )
			) * ( 1.0 / 9.0 );
		#elif defined( SHADOWMAP_TYPE_VSM )
			shadow = VSMShadow( shadowMap, shadowCoord.xy, shadowCoord.z );
		#else
			shadow = texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z );
		#endif
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	vec2 cubeToUV( vec3 v, float texelSizeY ) {
		vec3 absV = abs( v );
		float scaleToCube = 1.0 / max( absV.x, max( absV.y, absV.z ) );
		absV *= scaleToCube;
		v *= scaleToCube * ( 1.0 - 2.0 * texelSizeY );
		vec2 planar = v.xy;
		float almostATexel = 1.5 * texelSizeY;
		float almostOne = 1.0 - almostATexel;
		if ( absV.z >= almostOne ) {
			if ( v.z > 0.0 )
				planar.x = 4.0 - v.x;
		} else if ( absV.x >= almostOne ) {
			float signX = sign( v.x );
			planar.x = v.z * signX + 2.0 * signX;
		} else if ( absV.y >= almostOne ) {
			float signY = sign( v.y );
			planar.x = v.x + 2.0 * signY + 2.0;
			planar.y = v.z * signY - 2.0;
		}
		return vec2( 0.125, 0.25 ) * planar + vec2( 0.375, 0.75 );
	}
	float getPointShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		
		float lightToPositionLength = length( lightToPosition );
		if ( lightToPositionLength - shadowCameraFar <= 0.0 && lightToPositionLength - shadowCameraNear >= 0.0 ) {
			float dp = ( lightToPositionLength - shadowCameraNear ) / ( shadowCameraFar - shadowCameraNear );			dp += shadowBias;
			vec3 bd3D = normalize( lightToPosition );
			vec2 texelSize = vec2( 1.0 ) / ( shadowMapSize * vec2( 4.0, 2.0 ) );
			#if defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_PCF_SOFT ) || defined( SHADOWMAP_TYPE_VSM )
				vec2 offset = vec2( - 1, 1 ) * shadowRadius * texelSize.y;
				shadow = (
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxy, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxx, texelSize.y ), dp ) +
					texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxx, texelSize.y ), dp )
				) * ( 1.0 / 9.0 );
			#else
				shadow = texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp );
			#endif
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
#endif`,ja=`#if NUM_SPOT_LIGHT_COORDS > 0
	uniform mat4 spotLightMatrix[ NUM_SPOT_LIGHT_COORDS ];
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform mat4 directionalShadowMatrix[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform mat4 pointShadowMatrix[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
#endif`,tc=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
	vec3 shadowWorldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
	vec4 shadowWorldPosition;
#endif
#if defined( USE_SHADOWMAP )
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * directionalLightShadows[ i ].shadowNormalBias, 0 );
			vDirectionalShadowCoord[ i ] = directionalShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * pointLightShadows[ i ].shadowNormalBias, 0 );
			vPointShadowCoord[ i ] = pointShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
#endif
#if NUM_SPOT_LIGHT_COORDS > 0
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_COORDS; i ++ ) {
		shadowWorldPosition = worldPosition;
		#if ( defined( USE_SHADOWMAP ) && UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
			shadowWorldPosition.xyz += shadowWorldNormal * spotLightShadows[ i ].shadowNormalBias;
		#endif
		vSpotLightCoord[ i ] = spotLightMatrix[ i ] * shadowWorldPosition;
	}
	#pragma unroll_loop_end
#endif`,ec=`float getShadowMask() {
	float shadow = 1.0;
	#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
		directionalLight = directionalLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( directionalShadowMap[ i ], directionalLight.shadowMapSize, directionalLight.shadowIntensity, directionalLight.shadowBias, directionalLight.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_SHADOWS; i ++ ) {
		spotLight = spotLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( spotShadowMap[ i ], spotLight.shadowMapSize, spotLight.shadowIntensity, spotLight.shadowBias, spotLight.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
		pointLight = pointLightShadows[ i ];
		shadow *= receiveShadow ? getPointShadow( pointShadowMap[ i ], pointLight.shadowMapSize, pointLight.shadowIntensity, pointLight.shadowBias, pointLight.shadowRadius, vPointShadowCoord[ i ], pointLight.shadowCameraNear, pointLight.shadowCameraFar ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#endif
	return shadow;
}`,nc=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,ic=`#ifdef USE_SKINNING
	uniform mat4 bindMatrix;
	uniform mat4 bindMatrixInverse;
	uniform highp sampler2D boneTexture;
	mat4 getBoneMatrix( const in float i ) {
		int size = textureSize( boneTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( boneTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( boneTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( boneTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( boneTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
#endif`,sc=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,rc=`#ifdef USE_SKINNING
	mat4 skinMatrix = mat4( 0.0 );
	skinMatrix += skinWeight.x * boneMatX;
	skinMatrix += skinWeight.y * boneMatY;
	skinMatrix += skinWeight.z * boneMatZ;
	skinMatrix += skinWeight.w * boneMatW;
	skinMatrix = bindMatrixInverse * skinMatrix * bindMatrix;
	objectNormal = vec4( skinMatrix * vec4( objectNormal, 0.0 ) ).xyz;
	#ifdef USE_TANGENT
		objectTangent = vec4( skinMatrix * vec4( objectTangent, 0.0 ) ).xyz;
	#endif
#endif`,oc=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,ac=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,cc=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,lc=`#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
uniform float toneMappingExposure;
vec3 LinearToneMapping( vec3 color ) {
	return saturate( toneMappingExposure * color );
}
vec3 ReinhardToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	return saturate( color / ( vec3( 1.0 ) + color ) );
}
vec3 CineonToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	color = max( vec3( 0.0 ), color - 0.004 );
	return pow( ( color * ( 6.2 * color + 0.5 ) ) / ( color * ( 6.2 * color + 1.7 ) + 0.06 ), vec3( 2.2 ) );
}
vec3 RRTAndODTFit( vec3 v ) {
	vec3 a = v * ( v + 0.0245786 ) - 0.000090537;
	vec3 b = v * ( 0.983729 * v + 0.4329510 ) + 0.238081;
	return a / b;
}
vec3 ACESFilmicToneMapping( vec3 color ) {
	const mat3 ACESInputMat = mat3(
		vec3( 0.59719, 0.07600, 0.02840 ),		vec3( 0.35458, 0.90834, 0.13383 ),
		vec3( 0.04823, 0.01566, 0.83777 )
	);
	const mat3 ACESOutputMat = mat3(
		vec3(  1.60475, -0.10208, -0.00327 ),		vec3( -0.53108,  1.10813, -0.07276 ),
		vec3( -0.07367, -0.00605,  1.07602 )
	);
	color *= toneMappingExposure / 0.6;
	color = ACESInputMat * color;
	color = RRTAndODTFit( color );
	color = ACESOutputMat * color;
	return saturate( color );
}
const mat3 LINEAR_REC2020_TO_LINEAR_SRGB = mat3(
	vec3( 1.6605, - 0.1246, - 0.0182 ),
	vec3( - 0.5876, 1.1329, - 0.1006 ),
	vec3( - 0.0728, - 0.0083, 1.1187 )
);
const mat3 LINEAR_SRGB_TO_LINEAR_REC2020 = mat3(
	vec3( 0.6274, 0.0691, 0.0164 ),
	vec3( 0.3293, 0.9195, 0.0880 ),
	vec3( 0.0433, 0.0113, 0.8956 )
);
vec3 agxDefaultContrastApprox( vec3 x ) {
	vec3 x2 = x * x;
	vec3 x4 = x2 * x2;
	return + 15.5 * x4 * x2
		- 40.14 * x4 * x
		+ 31.96 * x4
		- 6.868 * x2 * x
		+ 0.4298 * x2
		+ 0.1191 * x
		- 0.00232;
}
vec3 AgXToneMapping( vec3 color ) {
	const mat3 AgXInsetMatrix = mat3(
		vec3( 0.856627153315983, 0.137318972929847, 0.11189821299995 ),
		vec3( 0.0951212405381588, 0.761241990602591, 0.0767994186031903 ),
		vec3( 0.0482516061458583, 0.101439036467562, 0.811302368396859 )
	);
	const mat3 AgXOutsetMatrix = mat3(
		vec3( 1.1271005818144368, - 0.1413297634984383, - 0.14132976349843826 ),
		vec3( - 0.11060664309660323, 1.157823702216272, - 0.11060664309660294 ),
		vec3( - 0.016493938717834573, - 0.016493938717834257, 1.2519364065950405 )
	);
	const float AgxMinEv = - 12.47393;	const float AgxMaxEv = 4.026069;
	color *= toneMappingExposure;
	color = LINEAR_SRGB_TO_LINEAR_REC2020 * color;
	color = AgXInsetMatrix * color;
	color = max( color, 1e-10 );	color = log2( color );
	color = ( color - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	color = clamp( color, 0.0, 1.0 );
	color = agxDefaultContrastApprox( color );
	color = AgXOutsetMatrix * color;
	color = pow( max( vec3( 0.0 ), color ), vec3( 2.2 ) );
	color = LINEAR_REC2020_TO_LINEAR_SRGB * color;
	color = clamp( color, 0.0, 1.0 );
	return color;
}
vec3 NeutralToneMapping( vec3 color ) {
	const float StartCompression = 0.8 - 0.04;
	const float Desaturation = 0.15;
	color *= toneMappingExposure;
	float x = min( color.r, min( color.g, color.b ) );
	float offset = x < 0.08 ? x - 6.25 * x * x : 0.04;
	color -= offset;
	float peak = max( color.r, max( color.g, color.b ) );
	if ( peak < StartCompression ) return color;
	float d = 1. - StartCompression;
	float newPeak = 1. - d * d / ( peak + d - StartCompression );
	color *= newPeak / peak;
	float g = 1. - 1. / ( Desaturation * ( peak - newPeak ) + 1. );
	return mix( color, vec3( newPeak ), g );
}
vec3 CustomToneMapping( vec3 color ) { return color; }`,uc=`#ifdef USE_TRANSMISSION
	material.transmission = transmission;
	material.transmissionAlpha = 1.0;
	material.thickness = thickness;
	material.attenuationDistance = attenuationDistance;
	material.attenuationColor = attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		material.transmission *= texture2D( transmissionMap, vTransmissionMapUv ).r;
	#endif
	#ifdef USE_THICKNESSMAP
		material.thickness *= texture2D( thicknessMap, vThicknessMapUv ).g;
	#endif
	vec3 pos = vWorldPosition;
	vec3 v = normalize( cameraPosition - pos );
	vec3 n = inverseTransformDirection( normal, viewMatrix );
	vec4 transmitted = getIBLVolumeRefraction(
		n, v, material.roughness, material.diffuseColor, material.specularColor, material.specularF90,
		pos, modelMatrix, viewMatrix, projectionMatrix, material.dispersion, material.ior, material.thickness,
		material.attenuationColor, material.attenuationDistance );
	material.transmissionAlpha = mix( material.transmissionAlpha, transmitted.a, material.transmission );
	totalDiffuse = mix( totalDiffuse, transmitted.rgb, material.transmission );
#endif`,hc=`#ifdef USE_TRANSMISSION
	uniform float transmission;
	uniform float thickness;
	uniform float attenuationDistance;
	uniform vec3 attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		uniform sampler2D transmissionMap;
	#endif
	#ifdef USE_THICKNESSMAP
		uniform sampler2D thicknessMap;
	#endif
	uniform vec2 transmissionSamplerSize;
	uniform sampler2D transmissionSamplerMap;
	uniform mat4 modelMatrix;
	uniform mat4 projectionMatrix;
	varying vec3 vWorldPosition;
	float w0( float a ) {
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - a + 3.0 ) - 3.0 ) + 1.0 );
	}
	float w1( float a ) {
		return ( 1.0 / 6.0 ) * ( a *  a * ( 3.0 * a - 6.0 ) + 4.0 );
	}
	float w2( float a ){
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - 3.0 * a + 3.0 ) + 3.0 ) + 1.0 );
	}
	float w3( float a ) {
		return ( 1.0 / 6.0 ) * ( a * a * a );
	}
	float g0( float a ) {
		return w0( a ) + w1( a );
	}
	float g1( float a ) {
		return w2( a ) + w3( a );
	}
	float h0( float a ) {
		return - 1.0 + w1( a ) / ( w0( a ) + w1( a ) );
	}
	float h1( float a ) {
		return 1.0 + w3( a ) / ( w2( a ) + w3( a ) );
	}
	vec4 bicubic( sampler2D tex, vec2 uv, vec4 texelSize, float lod ) {
		uv = uv * texelSize.zw + 0.5;
		vec2 iuv = floor( uv );
		vec2 fuv = fract( uv );
		float g0x = g0( fuv.x );
		float g1x = g1( fuv.x );
		float h0x = h0( fuv.x );
		float h1x = h1( fuv.x );
		float h0y = h0( fuv.y );
		float h1y = h1( fuv.y );
		vec2 p0 = ( vec2( iuv.x + h0x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p1 = ( vec2( iuv.x + h1x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p2 = ( vec2( iuv.x + h0x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		vec2 p3 = ( vec2( iuv.x + h1x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		return g0( fuv.y ) * ( g0x * textureLod( tex, p0, lod ) + g1x * textureLod( tex, p1, lod ) ) +
			g1( fuv.y ) * ( g0x * textureLod( tex, p2, lod ) + g1x * textureLod( tex, p3, lod ) );
	}
	vec4 textureBicubic( sampler2D sampler, vec2 uv, float lod ) {
		vec2 fLodSize = vec2( textureSize( sampler, int( lod ) ) );
		vec2 cLodSize = vec2( textureSize( sampler, int( lod + 1.0 ) ) );
		vec2 fLodSizeInv = 1.0 / fLodSize;
		vec2 cLodSizeInv = 1.0 / cLodSize;
		vec4 fSample = bicubic( sampler, uv, vec4( fLodSizeInv, fLodSize ), floor( lod ) );
		vec4 cSample = bicubic( sampler, uv, vec4( cLodSizeInv, cLodSize ), ceil( lod ) );
		return mix( fSample, cSample, fract( lod ) );
	}
	vec3 getVolumeTransmissionRay( const in vec3 n, const in vec3 v, const in float thickness, const in float ior, const in mat4 modelMatrix ) {
		vec3 refractionVector = refract( - v, normalize( n ), 1.0 / ior );
		vec3 modelScale;
		modelScale.x = length( vec3( modelMatrix[ 0 ].xyz ) );
		modelScale.y = length( vec3( modelMatrix[ 1 ].xyz ) );
		modelScale.z = length( vec3( modelMatrix[ 2 ].xyz ) );
		return normalize( refractionVector ) * thickness * modelScale;
	}
	float applyIorToRoughness( const in float roughness, const in float ior ) {
		return roughness * clamp( ior * 2.0 - 2.0, 0.0, 1.0 );
	}
	vec4 getTransmissionSample( const in vec2 fragCoord, const in float roughness, const in float ior ) {
		float lod = log2( transmissionSamplerSize.x ) * applyIorToRoughness( roughness, ior );
		return textureBicubic( transmissionSamplerMap, fragCoord.xy, lod );
	}
	vec3 volumeAttenuation( const in float transmissionDistance, const in vec3 attenuationColor, const in float attenuationDistance ) {
		if ( isinf( attenuationDistance ) ) {
			return vec3( 1.0 );
		} else {
			vec3 attenuationCoefficient = -log( attenuationColor ) / attenuationDistance;
			vec3 transmittance = exp( - attenuationCoefficient * transmissionDistance );			return transmittance;
		}
	}
	vec4 getIBLVolumeRefraction( const in vec3 n, const in vec3 v, const in float roughness, const in vec3 diffuseColor,
		const in vec3 specularColor, const in float specularF90, const in vec3 position, const in mat4 modelMatrix,
		const in mat4 viewMatrix, const in mat4 projMatrix, const in float dispersion, const in float ior, const in float thickness,
		const in vec3 attenuationColor, const in float attenuationDistance ) {
		vec4 transmittedLight;
		vec3 transmittance;
		#ifdef USE_DISPERSION
			float halfSpread = ( ior - 1.0 ) * 0.025 * dispersion;
			vec3 iors = vec3( ior - halfSpread, ior, ior + halfSpread );
			for ( int i = 0; i < 3; i ++ ) {
				vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, iors[ i ], modelMatrix );
				vec3 refractedRayExit = position + transmissionRay;
				vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
				vec2 refractionCoords = ndcPos.xy / ndcPos.w;
				refractionCoords += 1.0;
				refractionCoords /= 2.0;
				vec4 transmissionSample = getTransmissionSample( refractionCoords, roughness, iors[ i ] );
				transmittedLight[ i ] = transmissionSample[ i ];
				transmittedLight.a += transmissionSample.a;
				transmittance[ i ] = diffuseColor[ i ] * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance )[ i ];
			}
			transmittedLight.a /= 3.0;
		#else
			vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, ior, modelMatrix );
			vec3 refractedRayExit = position + transmissionRay;
			vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
			vec2 refractionCoords = ndcPos.xy / ndcPos.w;
			refractionCoords += 1.0;
			refractionCoords /= 2.0;
			transmittedLight = getTransmissionSample( refractionCoords, roughness, ior );
			transmittance = diffuseColor * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance );
		#endif
		vec3 attenuatedColor = transmittance * transmittedLight.rgb;
		vec3 F = EnvironmentBRDF( n, v, specularColor, specularF90, roughness );
		float transmittanceFactor = ( transmittance.r + transmittance.g + transmittance.b ) / 3.0;
		return vec4( ( 1.0 - F ) * attenuatedColor, 1.0 - ( 1.0 - transmittedLight.a ) * transmittanceFactor );
	}
#endif`,fc=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_SPECULARMAP
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,dc=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	uniform mat3 mapTransform;
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	uniform mat3 alphaMapTransform;
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	uniform mat3 lightMapTransform;
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	uniform mat3 aoMapTransform;
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	uniform mat3 bumpMapTransform;
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	uniform mat3 normalMapTransform;
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_DISPLACEMENTMAP
	uniform mat3 displacementMapTransform;
	varying vec2 vDisplacementMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	uniform mat3 emissiveMapTransform;
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	uniform mat3 metalnessMapTransform;
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	uniform mat3 roughnessMapTransform;
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	uniform mat3 anisotropyMapTransform;
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	uniform mat3 clearcoatMapTransform;
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform mat3 clearcoatNormalMapTransform;
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform mat3 clearcoatRoughnessMapTransform;
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	uniform mat3 sheenColorMapTransform;
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	uniform mat3 sheenRoughnessMapTransform;
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	uniform mat3 iridescenceMapTransform;
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform mat3 iridescenceThicknessMapTransform;
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SPECULARMAP
	uniform mat3 specularMapTransform;
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	uniform mat3 specularColorMapTransform;
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	uniform mat3 specularIntensityMapTransform;
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,pc=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	vUv = vec3( uv, 1 ).xy;
#endif
#ifdef USE_MAP
	vMapUv = ( mapTransform * vec3( MAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ALPHAMAP
	vAlphaMapUv = ( alphaMapTransform * vec3( ALPHAMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_LIGHTMAP
	vLightMapUv = ( lightMapTransform * vec3( LIGHTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_AOMAP
	vAoMapUv = ( aoMapTransform * vec3( AOMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_BUMPMAP
	vBumpMapUv = ( bumpMapTransform * vec3( BUMPMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_NORMALMAP
	vNormalMapUv = ( normalMapTransform * vec3( NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_DISPLACEMENTMAP
	vDisplacementMapUv = ( displacementMapTransform * vec3( DISPLACEMENTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_EMISSIVEMAP
	vEmissiveMapUv = ( emissiveMapTransform * vec3( EMISSIVEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_METALNESSMAP
	vMetalnessMapUv = ( metalnessMapTransform * vec3( METALNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ROUGHNESSMAP
	vRoughnessMapUv = ( roughnessMapTransform * vec3( ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ANISOTROPYMAP
	vAnisotropyMapUv = ( anisotropyMapTransform * vec3( ANISOTROPYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOATMAP
	vClearcoatMapUv = ( clearcoatMapTransform * vec3( CLEARCOATMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	vClearcoatNormalMapUv = ( clearcoatNormalMapTransform * vec3( CLEARCOAT_NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	vClearcoatRoughnessMapUv = ( clearcoatRoughnessMapTransform * vec3( CLEARCOAT_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCEMAP
	vIridescenceMapUv = ( iridescenceMapTransform * vec3( IRIDESCENCEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	vIridescenceThicknessMapUv = ( iridescenceThicknessMapTransform * vec3( IRIDESCENCE_THICKNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_COLORMAP
	vSheenColorMapUv = ( sheenColorMapTransform * vec3( SHEEN_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	vSheenRoughnessMapUv = ( sheenRoughnessMapTransform * vec3( SHEEN_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULARMAP
	vSpecularMapUv = ( specularMapTransform * vec3( SPECULARMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_COLORMAP
	vSpecularColorMapUv = ( specularColorMapTransform * vec3( SPECULAR_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	vSpecularIntensityMapUv = ( specularIntensityMapTransform * vec3( SPECULAR_INTENSITYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_TRANSMISSIONMAP
	vTransmissionMapUv = ( transmissionMapTransform * vec3( TRANSMISSIONMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_THICKNESSMAP
	vThicknessMapUv = ( thicknessMapTransform * vec3( THICKNESSMAP_UV, 1 ) ).xy;
#endif`,mc=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`,gc=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,_c=`uniform sampler2D t2D;
uniform float backgroundIntensity;
varying vec2 vUv;
void main() {
	vec4 texColor = texture2D( t2D, vUv );
	#ifdef DECODE_VIDEO_TEXTURE
		texColor = vec4( mix( pow( texColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), texColor.rgb * 0.0773993808, vec3( lessThanEqual( texColor.rgb, vec3( 0.04045 ) ) ) ), texColor.w );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,xc=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,yc=`#ifdef ENVMAP_TYPE_CUBE
	uniform samplerCube envMap;
#elif defined( ENVMAP_TYPE_CUBE_UV )
	uniform sampler2D envMap;
#endif
uniform float flipEnvMap;
uniform float backgroundBlurriness;
uniform float backgroundIntensity;
uniform mat3 backgroundRotation;
varying vec3 vWorldDirection;
#include <cube_uv_reflection_fragment>
void main() {
	#ifdef ENVMAP_TYPE_CUBE
		vec4 texColor = textureCube( envMap, backgroundRotation * vec3( flipEnvMap * vWorldDirection.x, vWorldDirection.yz ) );
	#elif defined( ENVMAP_TYPE_CUBE_UV )
		vec4 texColor = textureCubeUV( envMap, backgroundRotation * vWorldDirection, backgroundBlurriness );
	#else
		vec4 texColor = vec4( 0.0, 0.0, 0.0, 1.0 );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,vc=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,Mc=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Sc=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
varying vec2 vHighPrecisionZW;
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vHighPrecisionZW = gl_Position.zw;
}`,bc=`#if DEPTH_PACKING == 3200
	uniform float opacity;
#endif
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
varying vec2 vHighPrecisionZW;
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#if DEPTH_PACKING == 3200
		diffuseColor.a = opacity;
	#endif
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <logdepthbuf_fragment>
	#ifdef USE_REVERSED_DEPTH_BUFFER
		float fragCoordZ = vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ];
	#else
		float fragCoordZ = 0.5 * vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ] + 0.5;
	#endif
	#if DEPTH_PACKING == 3200
		gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );
	#elif DEPTH_PACKING == 3201
		gl_FragColor = packDepthToRGBA( fragCoordZ );
	#elif DEPTH_PACKING == 3202
		gl_FragColor = vec4( packDepthToRGB( fragCoordZ ), 1.0 );
	#elif DEPTH_PACKING == 3203
		gl_FragColor = vec4( packDepthToRG( fragCoordZ ), 0.0, 1.0 );
	#endif
}`,Tc=`#define DISTANCE
varying vec3 vWorldPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <worldpos_vertex>
	#include <clipping_planes_vertex>
	vWorldPosition = worldPosition.xyz;
}`,Ec=`#define DISTANCE
uniform vec3 referencePosition;
uniform float nearDistance;
uniform float farDistance;
varying vec3 vWorldPosition;
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <clipping_planes_pars_fragment>
void main () {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	float dist = length( vWorldPosition - referencePosition );
	dist = ( dist - nearDistance ) / ( farDistance - nearDistance );
	dist = saturate( dist );
	gl_FragColor = packDepthToRGBA( dist );
}`,Ac=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,wc=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Cc=`uniform float scale;
attribute float lineDistance;
varying float vLineDistance;
#include <common>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	vLineDistance = scale * lineDistance;
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,Rc=`uniform vec3 diffuse;
uniform float opacity;
uniform float dashSize;
uniform float totalSize;
varying float vLineDistance;
#include <common>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	if ( mod( vLineDistance, totalSize ) > dashSize ) {
		discard;
	}
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,Ic=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#if defined ( USE_ENVMAP ) || defined ( USE_SKINNING )
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinbase_vertex>
		#include <skinnormal_vertex>
		#include <defaultnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <fog_vertex>
}`,Pc=`uniform vec3 diffuse;
uniform float opacity;
#ifndef FLAT_SHADED
	varying vec3 vNormal;
#endif
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		reflectedLight.indirectDiffuse += lightMapTexel.rgb * lightMapIntensity * RECIPROCAL_PI;
	#else
		reflectedLight.indirectDiffuse += vec3( 1.0 );
	#endif
	#include <aomap_fragment>
	reflectedLight.indirectDiffuse *= diffuseColor.rgb;
	vec3 outgoingLight = reflectedLight.indirectDiffuse;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Dc=`#define LAMBERT
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Lc=`#define LAMBERT
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_lambert_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_lambert_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Uc=`#define MATCAP
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <displacementmap_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
	vViewPosition = - mvPosition.xyz;
}`,Nc=`#define MATCAP
uniform vec3 diffuse;
uniform float opacity;
uniform sampler2D matcap;
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	vec3 viewDir = normalize( vViewPosition );
	vec3 x = normalize( vec3( viewDir.z, 0.0, - viewDir.x ) );
	vec3 y = cross( viewDir, x );
	vec2 uv = vec2( dot( x, normal ), dot( y, normal ) ) * 0.495 + 0.5;
	#ifdef USE_MATCAP
		vec4 matcapColor = texture2D( matcap, uv );
	#else
		vec4 matcapColor = vec4( vec3( mix( 0.2, 0.8, uv.y ) ), 1.0 );
	#endif
	vec3 outgoingLight = diffuseColor.rgb * matcapColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Fc=`#define NORMAL
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	vViewPosition = - mvPosition.xyz;
#endif
}`,Bc=`#define NORMAL
uniform float opacity;
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <packing>
#include <uv_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 0.0, 0.0, 0.0, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	gl_FragColor = vec4( packNormalToRGB( normal ), diffuseColor.a );
	#ifdef OPAQUE
		gl_FragColor.a = 1.0;
	#endif
}`,Oc=`#define PHONG
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,zc=`#define PHONG
uniform vec3 diffuse;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_phong_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_phong_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + reflectedLight.directSpecular + reflectedLight.indirectSpecular + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Vc=`#define STANDARD
varying vec3 vViewPosition;
#ifdef USE_TRANSMISSION
	varying vec3 vWorldPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
#ifdef USE_TRANSMISSION
	vWorldPosition = worldPosition.xyz;
#endif
}`,kc=`#define STANDARD
#ifdef PHYSICAL
	#define IOR
	#define USE_SPECULAR
#endif
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;
#ifdef IOR
	uniform float ior;
#endif
#ifdef USE_SPECULAR
	uniform float specularIntensity;
	uniform vec3 specularColor;
	#ifdef USE_SPECULAR_COLORMAP
		uniform sampler2D specularColorMap;
	#endif
	#ifdef USE_SPECULAR_INTENSITYMAP
		uniform sampler2D specularIntensityMap;
	#endif
#endif
#ifdef USE_CLEARCOAT
	uniform float clearcoat;
	uniform float clearcoatRoughness;
#endif
#ifdef USE_DISPERSION
	uniform float dispersion;
#endif
#ifdef USE_IRIDESCENCE
	uniform float iridescence;
	uniform float iridescenceIOR;
	uniform float iridescenceThicknessMinimum;
	uniform float iridescenceThicknessMaximum;
#endif
#ifdef USE_SHEEN
	uniform vec3 sheenColor;
	uniform float sheenRoughness;
	#ifdef USE_SHEEN_COLORMAP
		uniform sampler2D sheenColorMap;
	#endif
	#ifdef USE_SHEEN_ROUGHNESSMAP
		uniform sampler2D sheenRoughnessMap;
	#endif
#endif
#ifdef USE_ANISOTROPY
	uniform vec2 anisotropyVector;
	#ifdef USE_ANISOTROPYMAP
		uniform sampler2D anisotropyMap;
	#endif
#endif
varying vec3 vViewPosition;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <iridescence_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_physical_pars_fragment>
#include <transmission_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <clearcoat_pars_fragment>
#include <iridescence_pars_fragment>
#include <roughnessmap_pars_fragment>
#include <metalnessmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <roughnessmap_fragment>
	#include <metalnessmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_physical_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 totalDiffuse = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse;
	vec3 totalSpecular = reflectedLight.directSpecular + reflectedLight.indirectSpecular;
	#include <transmission_fragment>
	vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;
	#ifdef USE_SHEEN
		float sheenEnergyComp = 1.0 - 0.157 * max3( material.sheenColor );
		outgoingLight = outgoingLight * sheenEnergyComp + sheenSpecularDirect + sheenSpecularIndirect;
	#endif
	#ifdef USE_CLEARCOAT
		float dotNVcc = saturate( dot( geometryClearcoatNormal, geometryViewDir ) );
		vec3 Fcc = F_Schlick( material.clearcoatF0, material.clearcoatF90, dotNVcc );
		outgoingLight = outgoingLight * ( 1.0 - material.clearcoat * Fcc ) + ( clearcoatSpecularDirect + clearcoatSpecularIndirect ) * material.clearcoat;
	#endif
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Hc=`#define TOON
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Gc=`#define TOON
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <gradientmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_toon_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_toon_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Wc=`uniform float size;
uniform float scale;
#include <common>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
#ifdef USE_POINTS_UV
	varying vec2 vUv;
	uniform mat3 uvTransform;
#endif
void main() {
	#ifdef USE_POINTS_UV
		vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	#endif
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	gl_PointSize = size;
	#ifdef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) gl_PointSize *= ( scale / - mvPosition.z );
	#endif
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <fog_vertex>
}`,Xc=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <color_pars_fragment>
#include <map_particle_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_particle_fragment>
	#include <color_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,qc=`#include <common>
#include <batching_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <shadowmap_pars_vertex>
void main() {
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Yc=`uniform vec3 color;
uniform float opacity;
#include <common>
#include <packing>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <logdepthbuf_pars_fragment>
#include <shadowmap_pars_fragment>
#include <shadowmask_pars_fragment>
void main() {
	#include <logdepthbuf_fragment>
	gl_FragColor = vec4( color, opacity * ( 1.0 - getShadowMask() ) );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,Zc=`uniform float rotation;
uniform vec2 center;
#include <common>
#include <uv_pars_vertex>
#include <fog_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	vec4 mvPosition = modelViewMatrix[ 3 ];
	vec2 scale = vec2( length( modelMatrix[ 0 ].xyz ), length( modelMatrix[ 1 ].xyz ) );
	#ifndef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) scale *= - mvPosition.z;
	#endif
	vec2 alignedPosition = ( position.xy - ( center - vec2( 0.5 ) ) ) * scale;
	vec2 rotatedPosition;
	rotatedPosition.x = cos( rotation ) * alignedPosition.x - sin( rotation ) * alignedPosition.y;
	rotatedPosition.y = sin( rotation ) * alignedPosition.x + cos( rotation ) * alignedPosition.y;
	mvPosition.xy += rotatedPosition;
	gl_Position = projectionMatrix * mvPosition;
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,Jc=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,F={alphahash_fragment:_o,alphahash_pars_fragment:xo,alphamap_fragment:yo,alphamap_pars_fragment:vo,alphatest_fragment:Mo,alphatest_pars_fragment:So,aomap_fragment:bo,aomap_pars_fragment:To,batching_pars_vertex:Eo,batching_vertex:Ao,begin_vertex:wo,beginnormal_vertex:Co,bsdfs:Ro,iridescence_fragment:Io,bumpmap_pars_fragment:Po,clipping_planes_fragment:Do,clipping_planes_pars_fragment:Lo,clipping_planes_pars_vertex:Uo,clipping_planes_vertex:No,color_fragment:Fo,color_pars_fragment:Bo,color_pars_vertex:Oo,color_vertex:zo,common:Vo,cube_uv_reflection_fragment:ko,defaultnormal_vertex:Ho,displacementmap_pars_vertex:Go,displacementmap_vertex:Wo,emissivemap_fragment:Xo,emissivemap_pars_fragment:qo,colorspace_fragment:Yo,colorspace_pars_fragment:Zo,envmap_fragment:Jo,envmap_common_pars_fragment:$o,envmap_pars_fragment:Ko,envmap_pars_vertex:Qo,envmap_physical_pars_fragment:la,envmap_vertex:jo,fog_vertex:ta,fog_pars_vertex:ea,fog_fragment:na,fog_pars_fragment:ia,gradientmap_pars_fragment:sa,lightmap_pars_fragment:ra,lights_lambert_fragment:oa,lights_lambert_pars_fragment:aa,lights_pars_begin:ca,lights_toon_fragment:ua,lights_toon_pars_fragment:ha,lights_phong_fragment:fa,lights_phong_pars_fragment:da,lights_physical_fragment:pa,lights_physical_pars_fragment:ma,lights_fragment_begin:ga,lights_fragment_maps:_a,lights_fragment_end:xa,logdepthbuf_fragment:ya,logdepthbuf_pars_fragment:va,logdepthbuf_pars_vertex:Ma,logdepthbuf_vertex:Sa,map_fragment:ba,map_pars_fragment:Ta,map_particle_fragment:Ea,map_particle_pars_fragment:Aa,metalnessmap_fragment:wa,metalnessmap_pars_fragment:Ca,morphinstance_vertex:Ra,morphcolor_vertex:Ia,morphnormal_vertex:Pa,morphtarget_pars_vertex:Da,morphtarget_vertex:La,normal_fragment_begin:Ua,normal_fragment_maps:Na,normal_pars_fragment:Fa,normal_pars_vertex:Ba,normal_vertex:Oa,normalmap_pars_fragment:za,clearcoat_normal_fragment_begin:Va,clearcoat_normal_fragment_maps:ka,clearcoat_pars_fragment:Ha,iridescence_pars_fragment:Ga,opaque_fragment:Wa,packing:Xa,premultiplied_alpha_fragment:qa,project_vertex:Ya,dithering_fragment:Za,dithering_pars_fragment:Ja,roughnessmap_fragment:$a,roughnessmap_pars_fragment:Ka,shadowmap_pars_fragment:Qa,shadowmap_pars_vertex:ja,shadowmap_vertex:tc,shadowmask_pars_fragment:ec,skinbase_vertex:nc,skinning_pars_vertex:ic,skinning_vertex:sc,skinnormal_vertex:rc,specularmap_fragment:oc,specularmap_pars_fragment:ac,tonemapping_fragment:cc,tonemapping_pars_fragment:lc,transmission_fragment:uc,transmission_pars_fragment:hc,uv_pars_fragment:fc,uv_pars_vertex:dc,uv_vertex:pc,worldpos_vertex:mc,background_vert:gc,background_frag:_c,backgroundCube_vert:xc,backgroundCube_frag:yc,cube_vert:vc,cube_frag:Mc,depth_vert:Sc,depth_frag:bc,distanceRGBA_vert:Tc,distanceRGBA_frag:Ec,equirect_vert:Ac,equirect_frag:wc,linedashed_vert:Cc,linedashed_frag:Rc,meshbasic_vert:Ic,meshbasic_frag:Pc,meshlambert_vert:Dc,meshlambert_frag:Lc,meshmatcap_vert:Uc,meshmatcap_frag:Nc,meshnormal_vert:Fc,meshnormal_frag:Bc,meshphong_vert:Oc,meshphong_frag:zc,meshphysical_vert:Vc,meshphysical_frag:kc,meshtoon_vert:Hc,meshtoon_frag:Gc,points_vert:Wc,points_frag:Xc,shadow_vert:qc,shadow_frag:Yc,sprite_vert:Zc,sprite_frag:Jc},P={common:{diffuse:{value:new tt(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new N},alphaMap:{value:null},alphaMapTransform:{value:new N},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new N}},envmap:{envMap:{value:null},envMapRotation:{value:new N},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new N}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new N}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new N},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new N},normalScale:{value:new G(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new N},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new N}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new N}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new N}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new tt(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new tt(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new N},alphaTest:{value:0},uvTransform:{value:new N}},sprite:{diffuse:{value:new tt(16777215)},opacity:{value:1},center:{value:new G(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new N},alphaMap:{value:null},alphaMapTransform:{value:new N},alphaTest:{value:0}}},Zs={basic:{uniforms:ot([P.common,P.specularmap,P.envmap,P.aomap,P.lightmap,P.fog]),vertexShader:F.meshbasic_vert,fragmentShader:F.meshbasic_frag},lambert:{uniforms:ot([P.common,P.specularmap,P.envmap,P.aomap,P.lightmap,P.emissivemap,P.bumpmap,P.normalmap,P.displacementmap,P.fog,P.lights,{emissive:{value:new tt(0)}}]),vertexShader:F.meshlambert_vert,fragmentShader:F.meshlambert_frag},phong:{uniforms:ot([P.common,P.specularmap,P.envmap,P.aomap,P.lightmap,P.emissivemap,P.bumpmap,P.normalmap,P.displacementmap,P.fog,P.lights,{emissive:{value:new tt(0)},specular:{value:new tt(1118481)},shininess:{value:30}}]),vertexShader:F.meshphong_vert,fragmentShader:F.meshphong_frag},standard:{uniforms:ot([P.common,P.envmap,P.aomap,P.lightmap,P.emissivemap,P.bumpmap,P.normalmap,P.displacementmap,P.roughnessmap,P.metalnessmap,P.fog,P.lights,{emissive:{value:new tt(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:F.meshphysical_vert,fragmentShader:F.meshphysical_frag},toon:{uniforms:ot([P.common,P.aomap,P.lightmap,P.emissivemap,P.bumpmap,P.normalmap,P.displacementmap,P.gradientmap,P.fog,P.lights,{emissive:{value:new tt(0)}}]),vertexShader:F.meshtoon_vert,fragmentShader:F.meshtoon_frag},matcap:{uniforms:ot([P.common,P.bumpmap,P.normalmap,P.displacementmap,P.fog,{matcap:{value:null}}]),vertexShader:F.meshmatcap_vert,fragmentShader:F.meshmatcap_frag},points:{uniforms:ot([P.points,P.fog]),vertexShader:F.points_vert,fragmentShader:F.points_frag},dashed:{uniforms:ot([P.common,P.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:F.linedashed_vert,fragmentShader:F.linedashed_frag},depth:{uniforms:ot([P.common,P.displacementmap]),vertexShader:F.depth_vert,fragmentShader:F.depth_frag},normal:{uniforms:ot([P.common,P.bumpmap,P.normalmap,P.displacementmap,{opacity:{value:1}}]),vertexShader:F.meshnormal_vert,fragmentShader:F.meshnormal_frag},sprite:{uniforms:ot([P.sprite,P.fog]),vertexShader:F.sprite_vert,fragmentShader:F.sprite_frag},background:{uniforms:{uvTransform:{value:new N},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:F.background_vert,fragmentShader:F.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new N}},vertexShader:F.backgroundCube_vert,fragmentShader:F.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:F.cube_vert,fragmentShader:F.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:F.equirect_vert,fragmentShader:F.equirect_frag},distanceRGBA:{uniforms:ot([P.common,P.displacementmap,{referencePosition:{value:new S},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:F.distanceRGBA_vert,fragmentShader:F.distanceRGBA_frag},shadow:{uniforms:ot([P.lights,P.fog,{color:{value:new tt(0)},opacity:{value:1}}]),vertexShader:F.shadow_vert,fragmentShader:F.shadow_frag}};Zs.physical={uniforms:ot([Zs.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new N},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new N},clearcoatNormalScale:{value:new G(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new N},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new N},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new N},sheen:{value:0},sheenColor:{value:new tt(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new N},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new N},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new N},transmissionSamplerSize:{value:new G},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new N},attenuationDistance:{value:0},attenuationColor:{value:new tt(0)},specularColor:{value:new tt(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new N},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new N},anisotropyVector:{value:new G},anisotropyMap:{value:null},anisotropyMapTransform:{value:new N}}]),vertexShader:F.meshphysical_vert,fragmentShader:F.meshphysical_frag};var ee=(1+Math.sqrt(5))/2,Se=1/ee,Xm=[new S(-ee,Se,0),new S(ee,Se,0),new S(-Se,0,ee),new S(Se,0,ee),new S(0,ee,-Se),new S(0,ee,Se),new S(-1,1,-1),new S(1,1,-1),new S(-1,1,1),new S(1,1,1)];var qm=new Float32Array(16),Ym=new Float32Array(9),Zm=new Float32Array(4);var Jm={[Gi]:Wi,[Xi]:Ji,[Yi]:$i,[qi]:Zi,[Wi]:Gi,[Ji]:Xi,[$i]:Yi,[Zi]:qi};var Js=Math.pow(2,-24),Ye=Symbol("SKIP_GENERATION"),On={strategy:0,maxDepth:40,maxLeafSize:10,useSharedArrayBuffer:!1,setBoundingBox:!0,onProgress:null,indirect:!1,verbose:!0,range:null,[Ye]:!1};var dt=class{constructor(){this.min=1/0,this.max=-1/0}setFromPointsField(t,e){let n=1/0,i=-1/0;for(let s=0,r=t.length;s<r;s++){let a=t[s][e];n=a<n?a:n,i=a>i?a:i}this.min=n,this.max=i}setFromPoints(t,e){let n=1/0,i=-1/0;for(let s=0,r=e.length;s<r;s++){let o=e[s],a=t.dot(o);n=a<n?a:n,i=a>i?a:i}this.min=n,this.max=i}isSeparated(t){return this.min>t.max||t.min>this.max}};dt.prototype.setFromBox=(function(){let h=new S;return function(e,n){let i=n.min,s=n.max,r=1/0,o=-1/0;for(let a=0;a<=1;a++)for(let c=0;c<=1;c++)for(let l=0;l<=1;l++){h.x=i.x*a+s.x*(1-a),h.y=i.y*c+s.y*(1-c),h.z=i.z*l+s.z*(1-l);let f=e.dot(h);r=Math.min(f,r),o=Math.max(f,o)}this.min=r,this.max=o}})();var $c=(function(){let h=new S,t=new S,e=new S;return function(i,s,r){let o=i.start,a=h,c=s.start,l=t;e.subVectors(o,c),h.subVectors(i.end,i.start),t.subVectors(s.end,s.start);let f=e.dot(l),u=l.dot(a),d=l.dot(l),p=e.dot(a),v=a.dot(a)*d-u*u,y,g;v!==0?y=(f*u-p*d)/v:y=0,g=(f+y*u)/d,r.x=y,r.y=g}})(),Ze=(function(){let h=new G,t=new S,e=new S;return function(i,s,r,o){$c(i,s,h);let a=h.x,c=h.y;if(a>=0&&a<=1&&c>=0&&c<=1){i.at(a,r),s.at(c,o);return}else if(a>=0&&a<=1){c<0?s.at(0,o):s.at(1,o),i.closestPointToPoint(o,!0,r);return}else if(c>=0&&c<=1){a<0?i.at(0,r):i.at(1,r),s.closestPointToPoint(r,!0,o);return}else{let l;a<0?l=i.start:l=i.end;let f;c<0?f=s.start:f=s.end;let u=t,d=e;if(i.closestPointToPoint(f,!0,t),s.closestPointToPoint(l,!0,e),u.distanceToSquared(f)<=d.distanceToSquared(l)){r.copy(u),o.copy(f);return}else{r.copy(l),o.copy(d);return}}}})(),$s=(function(){let h=new S,t=new S,e=new jt,n=new rt;return function(s,r){let{radius:o,center:a}=s,{a:c,b:l,c:f}=r;if(n.start=c,n.end=l,n.closestPointToPoint(a,!0,h).distanceTo(a)<=o||(n.start=c,n.end=f,n.closestPointToPoint(a,!0,h).distanceTo(a)<=o)||(n.start=l,n.end=f,n.closestPointToPoint(a,!0,h).distanceTo(a)<=o))return!0;let m=r.getPlane(e);if(Math.abs(m.distanceToPoint(a))<=o){let y=m.projectPoint(a,t);if(r.containsPoint(y))return!0}return!1}})();var Kc=["x","y","z"],Dt=1e-15,Ks=Dt*Dt;function _t(h){return Math.abs(h)<Dt}var et=class extends St{constructor(...t){super(...t),this.isExtendedTriangle=!0,this.satAxes=new Array(4).fill().map(()=>new S),this.satBounds=new Array(4).fill().map(()=>new dt),this.points=[this.a,this.b,this.c],this.plane=new jt,this.isDegenerateIntoSegment=!1,this.isDegenerateIntoPoint=!1,this.degenerateSegment=new rt,this.needsUpdate=!0}intersectsSphere(t){return $s(t,this)}update(){let t=this.a,e=this.b,n=this.c,i=this.points,s=this.satAxes,r=this.satBounds,o=s[0],a=r[0];this.getNormal(o),a.setFromPoints(o,i);let c=s[1],l=r[1];c.subVectors(t,e),l.setFromPoints(c,i);let f=s[2],u=r[2];f.subVectors(e,n),u.setFromPoints(f,i);let d=s[3],p=r[3];d.subVectors(n,t),p.setFromPoints(d,i);let m=c.length(),v=f.length(),y=d.length();this.isDegenerateIntoPoint=!1,this.isDegenerateIntoSegment=!1,m<Dt?v<Dt||y<Dt?this.isDegenerateIntoPoint=!0:(this.isDegenerateIntoSegment=!0,this.degenerateSegment.start.copy(t),this.degenerateSegment.end.copy(n)):v<Dt?y<Dt?this.isDegenerateIntoPoint=!0:(this.isDegenerateIntoSegment=!0,this.degenerateSegment.start.copy(e),this.degenerateSegment.end.copy(t)):y<Dt&&(this.isDegenerateIntoSegment=!0,this.degenerateSegment.start.copy(n),this.degenerateSegment.end.copy(e)),this.plane.setFromNormalAndCoplanarPoint(o,t),this.needsUpdate=!1}};et.prototype.closestPointToSegment=(function(){let h=new S,t=new S,e=new rt;return function(i,s=null,r=null){let{start:o,end:a}=i,c=this.points,l,f=1/0;for(let u=0;u<3;u++){let d=(u+1)%3;e.start.copy(c[u]),e.end.copy(c[d]),Ze(e,i,h,t),l=h.distanceToSquared(t),l<f&&(f=l,s&&s.copy(h),r&&r.copy(t))}return this.closestPointToPoint(o,h),l=o.distanceToSquared(h),l<f&&(f=l,s&&s.copy(h),r&&r.copy(o)),this.closestPointToPoint(a,h),l=a.distanceToSquared(h),l<f&&(f=l,s&&s.copy(h),r&&r.copy(a)),Math.sqrt(f)}})();et.prototype.intersectsTriangle=(function(){let h=new et,t=new dt,e=new dt,n=new S,i=new S,s=new S,r=new S,o=new rt,a=new rt,c=new S,l=new G,f=new G;function u(M,x,_,E){let b=n;!M.isDegenerateIntoPoint&&!M.isDegenerateIntoSegment?b.copy(M.plane.normal):b.copy(x.plane.normal);let T=M.satBounds,C=M.satAxes;for(let w=1;w<4;w++){let I=T[w],D=C[w];if(t.setFromPoints(D,x.points),I.isSeparated(t)||(r.copy(b).cross(D),t.setFromPoints(r,M.points),e.setFromPoints(r,x.points),t.isSeparated(e)))return!1}let A=x.satBounds,R=x.satAxes;for(let w=1;w<4;w++){let I=A[w],D=R[w];if(t.setFromPoints(D,M.points),I.isSeparated(t)||(r.crossVectors(b,D),t.setFromPoints(r,M.points),e.setFromPoints(r,x.points),t.isSeparated(e)))return!1}return _&&(E||console.warn("ExtendedTriangle.intersectsTriangle: Triangles are coplanar which does not support an output edge. Setting edge to 0, 0, 0."),_.start.set(0,0,0),_.end.set(0,0,0)),!0}function d(M,x,_,E,b,T,C,A,R,w,I){let D=C/(C-A);w.x=E+(b-E)*D,I.start.subVectors(x,M).multiplyScalar(D).add(M),D=C/(C-R),w.y=E+(T-E)*D,I.end.subVectors(_,M).multiplyScalar(D).add(M)}function p(M,x,_,E,b,T,C,A,R,w,I){if(b>0)d(M.c,M.a,M.b,E,x,_,R,C,A,w,I);else if(T>0)d(M.b,M.a,M.c,_,x,E,A,C,R,w,I);else if(A*R>0||C!=0)d(M.a,M.b,M.c,x,_,E,C,A,R,w,I);else if(A!=0)d(M.b,M.a,M.c,_,x,E,A,C,R,w,I);else if(R!=0)d(M.c,M.a,M.b,E,x,_,R,C,A,w,I);else return!0;return!1}function m(M,x,_,E){let b=x.degenerateSegment,T=M.plane.distanceToPoint(b.start),C=M.plane.distanceToPoint(b.end);return _t(T)?_t(C)?u(M,x,_,E):(_&&(_.start.copy(b.start),_.end.copy(b.start)),M.containsPoint(b.start)):_t(C)?(_&&(_.start.copy(b.end),_.end.copy(b.end)),M.containsPoint(b.end)):M.plane.intersectLine(b,n)!=null?(_&&(_.start.copy(n),_.end.copy(n)),M.containsPoint(n)):!1}function v(M,x,_){let E=x.a;return _t(M.plane.distanceToPoint(E))&&M.containsPoint(E)?(_&&(_.start.copy(E),_.end.copy(E)),!0):!1}function y(M,x,_){let E=M.degenerateSegment,b=x.a;return E.closestPointToPoint(b,!0,n),b.distanceToSquared(n)<Ks?(_&&(_.start.copy(b),_.end.copy(b)),!0):!1}function g(M,x,_,E){if(M.isDegenerateIntoSegment)if(x.isDegenerateIntoSegment){let b=M.degenerateSegment,T=x.degenerateSegment,C=i,A=s;b.delta(C),T.delta(A);let R=n.subVectors(T.start,b.start),w=C.x*A.y-C.y*A.x;if(_t(w))return!1;let I=(R.x*A.y-R.y*A.x)/w,D=-(C.x*R.y-C.y*R.x)/w;if(I<0||I>1||D<0||D>1)return!1;let L=b.start.z+C.z*I,W=T.start.z+A.z*D;return _t(L-W)?(_&&(_.start.copy(b.start).addScaledVector(C,I),_.end.copy(b.start).addScaledVector(C,I)),!0):!1}else return x.isDegenerateIntoPoint?y(M,x,_):m(x,M,_,E);else{if(M.isDegenerateIntoPoint)return x.isDegenerateIntoPoint?x.a.distanceToSquared(M.a)<Ks?(_&&(_.start.copy(M.a),_.end.copy(M.a)),!0):!1:x.isDegenerateIntoSegment?y(x,M,_):v(x,M,_);if(x.isDegenerateIntoPoint)return v(M,x,_);if(x.isDegenerateIntoSegment)return m(M,x,_,E)}}return function(x,_=null,E=!1){this.needsUpdate&&this.update(),x.isExtendedTriangle?x.needsUpdate&&x.update():(h.copy(x),h.update(),x=h);let b=g(this,x,_,E);if(b!==void 0)return b;let T=this.plane,C=x.plane,A=C.distanceToPoint(this.a),R=C.distanceToPoint(this.b),w=C.distanceToPoint(this.c);_t(A)&&(A=0),_t(R)&&(R=0),_t(w)&&(w=0);let I=A*R,D=A*w;if(I>0&&D>0)return!1;let L=T.distanceToPoint(x.a),W=T.distanceToPoint(x.b),Tt=T.distanceToPoint(x.c);_t(L)&&(L=0),_t(W)&&(W=0),_t(Tt)&&(Tt=0);let Zt=L*W,Jt=L*Tt;if(Zt>0&&Jt>0)return!1;i.copy(T.normal),s.copy(C.normal);let Ut=i.cross(s),Nt=0,ri=Math.abs(Ut.x),Es=Math.abs(Ut.y);Es>ri&&(ri=Es,Nt=1),Math.abs(Ut.z)>ri&&(Nt=2);let re=Kc[Nt],Br=this.a[re],Or=this.b[re],zr=this.c[re],Vr=x.a[re],kr=x.b[re],Hr=x.c[re];if(p(this,Br,Or,zr,I,D,A,R,w,l,o))return u(this,x,_,E);if(p(x,Vr,kr,Hr,Zt,Jt,L,W,Tt,f,a))return u(this,x,_,E);if(l.y<l.x){let oi=l.y;l.y=l.x,l.x=oi,c.copy(o.start),o.start.copy(o.end),o.end.copy(c)}if(f.y<f.x){let oi=f.y;f.y=f.x,f.x=oi,c.copy(a.start),a.start.copy(a.end),a.end.copy(c)}return l.y<f.x||f.y<l.x?!1:(_&&(f.x>l.x?_.start.copy(a.start):_.start.copy(o.start),f.y<l.y?_.end.copy(a.end):_.end.copy(o.end)),!0)}})();et.prototype.distanceToPoint=(function(){let h=new S;return function(e){return this.closestPointToPoint(e,h),e.distanceTo(h)}})();et.prototype.distanceToTriangle=(function(){let h=new S,t=new S,e=["a","b","c"],n=new rt,i=new rt;return function(r,o=null,a=null){let c=o||a?n:null;if(this.intersectsTriangle(r,c))return(o||a)&&(o&&c.getCenter(o),a&&c.getCenter(a)),0;let l=1/0;for(let f=0;f<3;f++){let u,d=e[f],p=r[d];this.closestPointToPoint(p,h),u=p.distanceToSquared(h),u<l&&(l=u,o&&o.copy(h),a&&a.copy(p));let m=this[d];r.closestPointToPoint(m,h),u=m.distanceToSquared(h),u<l&&(l=u,o&&o.copy(m),a&&a.copy(h))}for(let f=0;f<3;f++){let u=e[f],d=e[(f+1)%3];n.set(this[u],this[d]);for(let p=0;p<3;p++){let m=e[p],v=e[(p+1)%3];i.set(r[m],r[v]),Ze(n,i,h,t);let y=h.distanceToSquared(t);y<l&&(l=y,o&&o.copy(h),a&&a.copy(t))}}return Math.sqrt(l)}})();var Z=class{constructor(t,e,n){this.isOrientedBox=!0,this.min=new S,this.max=new S,this.matrix=new q,this.invMatrix=new q,this.points=new Array(8).fill().map(()=>new S),this.satAxes=new Array(3).fill().map(()=>new S),this.satBounds=new Array(3).fill().map(()=>new dt),this.alignedSatBounds=new Array(3).fill().map(()=>new dt),this.needsUpdate=!1,t&&this.min.copy(t),e&&this.max.copy(e),n&&this.matrix.copy(n)}set(t,e,n){this.min.copy(t),this.max.copy(e),this.matrix.copy(n),this.needsUpdate=!0}copy(t){this.min.copy(t.min),this.max.copy(t.max),this.matrix.copy(t.matrix),this.needsUpdate=!0}};Z.prototype.update=(function(){return function(){let t=this.matrix,e=this.min,n=this.max,i=this.points;for(let c=0;c<=1;c++)for(let l=0;l<=1;l++)for(let f=0;f<=1;f++){let u=1*c|2*l|4*f,d=i[u];d.x=c?n.x:e.x,d.y=l?n.y:e.y,d.z=f?n.z:e.z,d.applyMatrix4(t)}let s=this.satBounds,r=this.satAxes,o=i[0];for(let c=0;c<3;c++){let l=r[c],f=s[c],u=1<<c,d=i[u];l.subVectors(o,d),f.setFromPoints(l,i)}let a=this.alignedSatBounds;a[0].setFromPointsField(i,"x"),a[1].setFromPointsField(i,"y"),a[2].setFromPointsField(i,"z"),this.invMatrix.copy(this.matrix).invert(),this.needsUpdate=!1}})();Z.prototype.intersectsBox=(function(){let h=new dt;return function(e){this.needsUpdate&&this.update();let n=e.min,i=e.max,s=this.satBounds,r=this.satAxes,o=this.alignedSatBounds;if(h.min=n.x,h.max=i.x,o[0].isSeparated(h)||(h.min=n.y,h.max=i.y,o[1].isSeparated(h))||(h.min=n.z,h.max=i.z,o[2].isSeparated(h)))return!1;for(let a=0;a<3;a++){let c=r[a],l=s[a];if(h.setFromBox(c,e),l.isSeparated(h))return!1}return!0}})();Z.prototype.intersectsTriangle=(function(){let h=new et,t=new Array(3),e=new dt,n=new dt,i=new S;return function(r){this.needsUpdate&&this.update(),r.isExtendedTriangle?r.needsUpdate&&r.update():(h.copy(r),h.update(),r=h);let o=this.satBounds,a=this.satAxes;t[0]=r.a,t[1]=r.b,t[2]=r.c;for(let u=0;u<3;u++){let d=o[u],p=a[u];if(e.setFromPoints(p,t),d.isSeparated(e))return!1}let c=r.satBounds,l=r.satAxes,f=this.points;for(let u=0;u<3;u++){let d=c[u],p=l[u];if(e.setFromPoints(p,f),d.isSeparated(e))return!1}for(let u=0;u<3;u++){let d=a[u];for(let p=0;p<4;p++){let m=l[p];if(i.crossVectors(d,m),e.setFromPoints(i,t),n.setFromPoints(i,f),e.isSeparated(n))return!1}}return!0}})();Z.prototype.closestPointToPoint=(function(){return function(t,e){return this.needsUpdate&&this.update(),e.copy(t).applyMatrix4(this.invMatrix).clamp(this.min,this.max).applyMatrix4(this.matrix),e}})();Z.prototype.distanceToPoint=(function(){let h=new S;return function(e){return this.closestPointToPoint(e,h),e.distanceTo(h)}})();Z.prototype.distanceToBox=(function(){let h=["x","y","z"],t=new Array(12).fill().map(()=>new rt),e=new Array(12).fill().map(()=>new rt),n=new S,i=new S;return function(r,o=0,a=null,c=null){if(this.needsUpdate&&this.update(),this.intersectsBox(r))return(a||c)&&(r.getCenter(i),this.closestPointToPoint(i,n),r.closestPointToPoint(n,i),a&&a.copy(n),c&&c.copy(i)),0;let l=o*o,f=r.min,u=r.max,d=this.points,p=1/0;for(let v=0;v<8;v++){let y=d[v];i.copy(y).clamp(f,u);let g=y.distanceToSquared(i);if(g<p&&(p=g,a&&a.copy(y),c&&c.copy(i),g<l))return Math.sqrt(g)}let m=0;for(let v=0;v<3;v++)for(let y=0;y<=1;y++)for(let g=0;g<=1;g++){let M=(v+1)%3,x=(v+2)%3,_=y<<M|g<<x,E=1<<v|y<<M|g<<x,b=d[_],T=d[E];t[m].set(b,T);let A=h[v],R=h[M],w=h[x],I=e[m],D=I.start,L=I.end;D[A]=f[A],D[R]=y?f[R]:u[R],D[w]=g?f[w]:u[R],L[A]=u[A],L[R]=y?f[R]:u[R],L[w]=g?f[w]:u[R],m++}for(let v=0;v<=1;v++)for(let y=0;y<=1;y++)for(let g=0;g<=1;g++){i.x=v?u.x:f.x,i.y=y?u.y:f.y,i.z=g?u.z:f.z,this.closestPointToPoint(i,n);let M=i.distanceToSquared(n);if(M<p&&(p=M,a&&a.copy(n),c&&c.copy(i),M<l))return Math.sqrt(M)}for(let v=0;v<12;v++){let y=t[v];for(let g=0;g<12;g++){let M=e[g];Ze(y,M,n,i);let x=n.distanceToSquared(i);if(x<p&&(p=x,a&&a.copy(n),c&&c.copy(i),x<l))return Math.sqrt(x)}}return Math.sqrt(p)}})();var Gt=class{constructor(t){this._getNewPrimitive=t,this._primitives=[]}getPrimitive(){let t=this._primitives;return t.length===0?this._getNewPrimitive():t.pop()}releasePrimitive(t){this._primitives.push(t)}};var ns=class extends Gt{constructor(){super(()=>new et)}},at=new ns;var Je=new S,is=new S;function Qs(h,t,e={},n=0,i=1/0){let s=n*n,r=i*i,o=1/0,a=null;if(h.shapecast({boundsTraverseOrder:l=>(Je.copy(t).clamp(l.min,l.max),Je.distanceToSquared(t)),intersectsBounds:(l,f,u)=>u<o&&u<r,intersectsTriangle:(l,f)=>{l.closestPointToPoint(t,Je);let u=t.distanceToSquared(Je);return u<o&&(is.copy(Je),o=u,a=f),u<s}}),o===1/0)return null;let c=Math.sqrt(o);return e.point?e.point.copy(is):e.point=is.clone(),e.distance=c,e.faceIndex=a,e}function O(h,t){return t[h+15]===65535}function J(h,t){return t[h+6]}function K(h,t){return t[h+14]}function z(h){return h+8}function V(h,t){let e=t[h+6];return h+e*8}function be(h,t){return t[h+7]}var zn=parseInt("180")>=169,jc=parseInt("180")<=161,ne=new S,ie=new S,se=new S,Vn=new G,kn=new G,Hn=new G,js=new S,tr=new S,er=new S,$e=new S;function tl(h,t,e,n,i,s,r,o){let a;if(s===ki?a=h.intersectTriangle(n,e,t,!0,i):a=h.intersectTriangle(t,e,n,s!==Hi,i),a===null)return null;let c=h.origin.distanceTo(i);return c<r||c>o?null:{distance:c,point:i.clone()}}function nr(h,t,e,n,i,s,r,o,a,c,l){ne.fromBufferAttribute(t,s),ie.fromBufferAttribute(t,r),se.fromBufferAttribute(t,o);let f=tl(h,ne,ie,se,$e,a,c,l);if(f){if(n){Vn.fromBufferAttribute(n,s),kn.fromBufferAttribute(n,r),Hn.fromBufferAttribute(n,o),f.uv=new G;let d=St.getInterpolation($e,ne,ie,se,Vn,kn,Hn,f.uv);zn||(f.uv=d)}if(i){Vn.fromBufferAttribute(i,s),kn.fromBufferAttribute(i,r),Hn.fromBufferAttribute(i,o),f.uv1=new G;let d=St.getInterpolation($e,ne,ie,se,Vn,kn,Hn,f.uv1);zn||(f.uv1=d),jc&&(f.uv2=f.uv1)}if(e){js.fromBufferAttribute(e,s),tr.fromBufferAttribute(e,r),er.fromBufferAttribute(e,o),f.normal=new S;let d=St.getInterpolation($e,ne,ie,se,js,tr,er,f.normal);f.normal.dot(h.direction)>0&&f.normal.multiplyScalar(-1),zn||(f.normal=d)}let u={a:s,b:r,c:o,normal:new S,materialIndex:0};if(St.getNormal(ne,ie,se,u.normal),f.face=u,f.faceIndex=s,zn){let d=new S;St.getBarycoord($e,ne,ie,se,d),f.barycoord=d}}return f}function ir(h){return h&&h.isMaterial?h.side:h}function Te(h,t,e,n,i,s,r){let o=n*3,a=o+0,c=o+1,l=o+2,{index:f,groups:u}=h;h.index&&(a=f.getX(a),c=f.getX(c),l=f.getX(l));let{position:d,normal:p,uv:m,uv1:v}=h.attributes;if(Array.isArray(t)){let y=n*3;for(let g=0,M=u.length;g<M;g++){let{start:x,count:_,materialIndex:E}=u[g];if(y>=x&&y<x+_){let b=ir(t[E]),T=nr(e,d,p,m,v,a,c,l,b,s,r);if(T)if(T.faceIndex=n,T.face.materialIndex=E,i)i.push(T);else return T}}}else{let y=ir(t),g=nr(e,d,p,m,v,a,c,l,y,s,r);if(g)if(g.faceIndex=n,g.face.materialIndex=0,i)i.push(g);else return g}return null}function k(h,t,e,n){let i=h.a,s=h.b,r=h.c,o=t,a=t+1,c=t+2;e&&(o=e.getX(o),a=e.getX(a),c=e.getX(c)),i.x=n.getX(o),i.y=n.getY(o),i.z=n.getZ(o),s.x=n.getX(a),s.y=n.getY(a),s.z=n.getZ(a),r.x=n.getX(c),r.y=n.getY(c),r.z=n.getZ(c)}function sr(h,t,e,n,i,s,r,o){let{geometry:a,_indirectBuffer:c}=h;for(let l=n,f=n+i;l<f;l++)Te(a,t,e,l,s,r,o)}function rr(h,t,e,n,i,s,r){let{geometry:o,_indirectBuffer:a}=h,c=1/0,l=null;for(let f=n,u=n+i;f<u;f++){let d;d=Te(o,t,e,f,null,s,r),d&&d.distance<c&&(l=d,c=d.distance)}return l}function or(h,t,e,n,i,s,r){let{geometry:o}=e,{index:a}=o,c=o.attributes.position;for(let l=h,f=t+h;l<f;l++){let u;if(u=l,k(r,u*3,a,c),r.needsUpdate=!0,n(r,u,i,s))return!0}return!1}function ar(h,t=null){t&&Array.isArray(t)&&(t=new Set(t));let e=h.geometry,n=e.index?e.index.array:null,i=e.attributes.position,s,r,o,a,c=0,l=h._roots;for(let u=0,d=l.length;u<d;u++)s=l[u],r=new Uint32Array(s),o=new Uint16Array(s),a=new Float32Array(s),f(0,c),c+=s.byteLength;function f(u,d,p=!1){let m=u*2;if(O(m,o)){let v=r[u+6],y=o[m+14],g=1/0,M=1/0,x=1/0,_=-1/0,E=-1/0,b=-1/0;for(let T=3*v,C=3*(v+y);T<C;T++){let A=n[T],R=i.getX(A),w=i.getY(A),I=i.getZ(A);R<g&&(g=R),R>_&&(_=R),w<M&&(M=w),w>E&&(E=w),I<x&&(x=I),I>b&&(b=I)}return a[u+0]!==g||a[u+1]!==M||a[u+2]!==x||a[u+3]!==_||a[u+4]!==E||a[u+5]!==b?(a[u+0]=g,a[u+1]=M,a[u+2]=x,a[u+3]=_,a[u+4]=E,a[u+5]=b,!0):!1}else{let v=z(u),y=V(u,r),g=p,M=!1,x=!1;if(t){if(!g){let A=v/8+d/32,R=y/8+d/32;M=t.has(A),x=t.has(R),g=!M&&!x}}else M=!0,x=!0;let _=g||M,E=g||x,b=!1;_&&(b=f(v,d,g));let T=!1;E&&(T=f(y,d,g));let C=b||T;if(C)for(let A=0;A<3;A++){let R=v+A,w=y+A,I=a[R],D=a[R+3],L=a[w],W=a[w+3];a[u+A]=I<L?I:L,a[u+A+3]=D>W?D:W}return C}}}function xt(h,t,e,n,i){let s,r,o,a,c,l,f=1/e.direction.x,u=1/e.direction.y,d=1/e.direction.z,p=e.origin.x,m=e.origin.y,v=e.origin.z,y=t[h],g=t[h+3],M=t[h+1],x=t[h+3+1],_=t[h+2],E=t[h+3+2];return f>=0?(s=(y-p)*f,r=(g-p)*f):(s=(g-p)*f,r=(y-p)*f),u>=0?(o=(M-m)*u,a=(x-m)*u):(o=(x-m)*u,a=(M-m)*u),s>a||o>r||((o>s||isNaN(s))&&(s=o),(a<r||isNaN(r))&&(r=a),d>=0?(c=(_-v)*d,l=(E-v)*d):(c=(E-v)*d,l=(_-v)*d),s>l||c>r)?!1:((c>s||s!==s)&&(s=c),(l<r||r!==r)&&(r=l),s<=i&&r>=n)}var ss=class{constructor(){this.float32Array=null,this.uint16Array=null,this.uint32Array=null;let t=[],e=null;this.setBuffer=n=>{e&&t.push(e),e=n,this.float32Array=new Float32Array(n),this.uint16Array=new Uint16Array(n),this.uint32Array=new Uint32Array(n)},this.clearBuffer=()=>{e=null,this.float32Array=null,this.uint16Array=null,this.uint32Array=null,t.length!==0&&this.setBuffer(t.pop())}}},B=new ss;function cr(h,t,e,n,i,s,r,o){let{geometry:a,_indirectBuffer:c}=h;for(let l=n,f=n+i;l<f;l++){let u=c?c[l]:l;Te(a,t,e,u,s,r,o)}}function lr(h,t,e,n,i,s,r){let{geometry:o,_indirectBuffer:a}=h,c=1/0,l=null;for(let f=n,u=n+i;f<u;f++){let d;d=Te(o,t,e,a?a[f]:f,null,s,r),d&&d.distance<c&&(l=d,c=d.distance)}return l}function ur(h,t,e,n,i,s,r){let{geometry:o}=e,{index:a}=o,c=o.attributes.position;for(let l=h,f=t+h;l<f;l++){let u;if(u=e.resolveTriangleIndex(l),k(r,u*3,a,c),r.needsUpdate=!0,n(r,u,i,s))return!0}return!1}function hr(h,t,e,n,i,s,r){B.setBuffer(h._roots[t]),rs(0,h,e,n,i,s,r),B.clearBuffer()}function rs(h,t,e,n,i,s,r){let{float32Array:o,uint16Array:a,uint32Array:c}=B,l=h*2;if(O(l,a)){let u=J(h,c),d=K(l,a);sr(t,e,n,u,d,i,s,r)}else{let u=z(h);xt(u,o,n,s,r)&&rs(u,t,e,n,i,s,r);let d=V(h,c);xt(d,o,n,s,r)&&rs(d,t,e,n,i,s,r)}}var el=["x","y","z"];function fr(h,t,e,n,i,s){B.setBuffer(h._roots[t]);let r=os(0,h,e,n,i,s);return B.clearBuffer(),r}function os(h,t,e,n,i,s){let{float32Array:r,uint16Array:o,uint32Array:a}=B,c=h*2;if(O(c,o)){let f=J(h,a),u=K(c,o);return rr(t,e,n,f,u,i,s)}else{let f=be(h,a),u=el[f],p=n.direction[u]>=0,m,v;p?(m=z(h),v=V(h,a)):(m=V(h,a),v=z(h));let g=xt(m,r,n,i,s)?os(m,t,e,n,i,s):null;if(g){let _=g.point[u];if(p?_<=r[v+f]:_>=r[v+f+3])return g}let x=xt(v,r,n,i,s)?os(v,t,e,n,i,s):null;return g&&x?g.distance<=x.distance?g:x:g||x||null}}function H(h,t,e){return e.min.x=t[h],e.min.y=t[h+1],e.min.z=t[h+2],e.max.x=t[h+3],e.max.y=t[h+4],e.max.z=t[h+5],e}function as(h){let t=-1,e=-1/0;for(let n=0;n<3;n++){let i=h[n+3]-h[n];i>e&&(e=i,t=n)}return t}function cs(h,t){t.set(h)}function ls(h,t,e){let n,i;for(let s=0;s<3;s++){let r=s+3;n=h[s],i=t[s],e[s]=n<i?n:i,n=h[r],i=t[r],e[r]=n>i?n:i}}function Ke(h,t,e){for(let n=0;n<3;n++){let i=t[h+2*n],s=t[h+2*n+1],r=i-s,o=i+s;r<e[n]&&(e[n]=r),o>e[n+3]&&(e[n+3]=o)}}function Ee(h){let t=h[3]-h[0],e=h[4]-h[1],n=h[5]-h[2];return 2*(t*e+e*n+n*t)}function us(h){return h.index?h.index.count:h.attributes.position.count}function Wt(h){return us(h)/3}function nl(h,t=ArrayBuffer){return h>65535?new Uint32Array(new t(4*h)):new Uint16Array(new t(2*h))}function dr(h,t){if(!h.index){let e=h.attributes.position.count,n=t.useSharedArrayBuffer?SharedArrayBuffer:ArrayBuffer,i=nl(e,n);h.setIndex(new st(i,1));for(let s=0;s<e;s++)i[s]=s}}function il(h,t,e){let n=us(h)/e,i=t||h.drawRange,s=i.start/e,r=(i.start+i.count)/e,o=Math.max(0,s),a=Math.min(n,r)-o;return{offset:Math.floor(o),count:Math.floor(a)}}function sl(h,t){return h.groups.map(e=>({offset:e.start/t,count:e.count/t}))}function Qe(h,t,e){let n=il(h,t,e),i=sl(h,e);if(!i.length)return[n];let s=[],r=n.offset,o=n.offset+n.count,a=us(h)/e,c=[];for(let u of i){let{offset:d,count:p}=u,m=d,v=isFinite(p)?p:a-d,y=d+v;m<o&&y>r&&(c.push({pos:Math.max(r,m),isStart:!0}),c.push({pos:Math.min(o,y),isStart:!1}))}c.sort((u,d)=>u.pos!==d.pos?u.pos-d.pos:u.type==="end"?-1:1);let l=0,f=null;for(let u of c){let d=u.pos;l!==0&&d!==f&&s.push({offset:f,count:d-f}),l+=u.isStart?1:-1,f=d}return s}var Gn=new Y,Ae=new et,we=new et,je=new q,pr=new Z,Wn=new Z;function mr(h,t,e,n){B.setBuffer(h._roots[t]);let i=hs(0,h,e,n);return B.clearBuffer(),i}function hs(h,t,e,n,i=null){let{float32Array:s,uint16Array:r,uint32Array:o}=B,a=h*2;if(i===null&&(e.boundingBox||e.computeBoundingBox(),pr.set(e.boundingBox.min,e.boundingBox.max,n),i=pr),O(a,r)){let l=t.geometry,f=l.index,u=l.attributes.position,d=e.index,p=e.attributes.position,m=J(h,o),v=K(a,r);if(je.copy(n).invert(),e.boundsTree)return H(h,s,Wn),Wn.matrix.copy(je),Wn.needsUpdate=!0,e.boundsTree.shapecast({intersectsBounds:g=>Wn.intersectsBox(g),intersectsTriangle:g=>{g.a.applyMatrix4(n),g.b.applyMatrix4(n),g.c.applyMatrix4(n),g.needsUpdate=!0;for(let M=m*3,x=(v+m)*3;M<x;M+=3)if(k(we,M,f,u),we.needsUpdate=!0,g.intersectsTriangle(we))return!0;return!1}});{let y=Wt(e);for(let g=m*3,M=(v+m)*3;g<M;g+=3){k(Ae,g,f,u),Ae.a.applyMatrix4(je),Ae.b.applyMatrix4(je),Ae.c.applyMatrix4(je),Ae.needsUpdate=!0;for(let x=0,_=y*3;x<_;x+=3)if(k(we,x,d,p),we.needsUpdate=!0,Ae.intersectsTriangle(we))return!0}}}else{let l=z(h),f=V(h,o);return H(l,s,Gn),!!(i.intersectsBox(Gn)&&hs(l,t,e,n,i)||(H(f,s,Gn),i.intersectsBox(Gn)&&hs(f,t,e,n,i)))}}var Xn=new q,ds=new Z,tn=new Z,rl=new S,ol=new S,al=new S,cl=new S;function gr(h,t,e,n={},i={},s=0,r=1/0){t.boundingBox||t.computeBoundingBox(),ds.set(t.boundingBox.min,t.boundingBox.max,e),ds.needsUpdate=!0;let o=h.geometry,a=o.attributes.position,c=o.index,l=t.attributes.position,f=t.index,u=at.getPrimitive(),d=at.getPrimitive(),p=rl,m=ol,v=null,y=null;i&&(v=al,y=cl);let g=1/0,M=null,x=null;return Xn.copy(e).invert(),tn.matrix.copy(Xn),h.shapecast({boundsTraverseOrder:_=>ds.distanceToBox(_),intersectsBounds:(_,E,b)=>b<g&&b<r?(E&&(tn.min.copy(_.min),tn.max.copy(_.max),tn.needsUpdate=!0),!0):!1,intersectsRange:(_,E)=>{if(t.boundsTree)return t.boundsTree.shapecast({boundsTraverseOrder:T=>tn.distanceToBox(T),intersectsBounds:(T,C,A)=>A<g&&A<r,intersectsRange:(T,C)=>{for(let A=T,R=T+C;A<R;A++){k(d,3*A,f,l),d.a.applyMatrix4(e),d.b.applyMatrix4(e),d.c.applyMatrix4(e),d.needsUpdate=!0;for(let w=_,I=_+E;w<I;w++){k(u,3*w,c,a),u.needsUpdate=!0;let D=u.distanceToTriangle(d,p,v);if(D<g&&(m.copy(p),y&&y.copy(v),g=D,M=w,x=A),D<s)return!0}}}});{let b=Wt(t);for(let T=0,C=b;T<C;T++){k(d,3*T,f,l),d.a.applyMatrix4(e),d.b.applyMatrix4(e),d.c.applyMatrix4(e),d.needsUpdate=!0;for(let A=_,R=_+E;A<R;A++){k(u,3*A,c,a),u.needsUpdate=!0;let w=u.distanceToTriangle(d,p,v);if(w<g&&(m.copy(p),y&&y.copy(v),g=w,M=A,x=T),w<s)return!0}}}}}),at.releasePrimitive(u),at.releasePrimitive(d),g===1/0?null:(n.point?n.point.copy(m):n.point=m.clone(),n.distance=g,n.faceIndex=M,i&&(i.point?i.point.copy(y):i.point=y.clone(),i.point.applyMatrix4(Xn),m.applyMatrix4(Xn),i.distance=m.sub(i.point).length(),i.faceIndex=x),n)}function _r(h,t=null){t&&Array.isArray(t)&&(t=new Set(t));let e=h.geometry,n=e.index?e.index.array:null,i=e.attributes.position,s,r,o,a,c=0,l=h._roots;for(let u=0,d=l.length;u<d;u++)s=l[u],r=new Uint32Array(s),o=new Uint16Array(s),a=new Float32Array(s),f(0,c),c+=s.byteLength;function f(u,d,p=!1){let m=u*2;if(O(m,o)){let v=r[u+6],y=o[m+14],g=1/0,M=1/0,x=1/0,_=-1/0,E=-1/0,b=-1/0;for(let T=v,C=v+y;T<C;T++){let A=3*h.resolveTriangleIndex(T);for(let R=0;R<3;R++){let w=A+R;w=n?n[w]:w;let I=i.getX(w),D=i.getY(w),L=i.getZ(w);I<g&&(g=I),I>_&&(_=I),D<M&&(M=D),D>E&&(E=D),L<x&&(x=L),L>b&&(b=L)}}return a[u+0]!==g||a[u+1]!==M||a[u+2]!==x||a[u+3]!==_||a[u+4]!==E||a[u+5]!==b?(a[u+0]=g,a[u+1]=M,a[u+2]=x,a[u+3]=_,a[u+4]=E,a[u+5]=b,!0):!1}else{let v=z(u),y=V(u,r),g=p,M=!1,x=!1;if(t){if(!g){let A=v/8+d/32,R=y/8+d/32;M=t.has(A),x=t.has(R),g=!M&&!x}}else M=!0,x=!0;let _=g||M,E=g||x,b=!1;_&&(b=f(v,d,g));let T=!1;E&&(T=f(y,d,g));let C=b||T;if(C)for(let A=0;A<3;A++){let R=v+A,w=y+A,I=a[R],D=a[R+3],L=a[w],W=a[w+3];a[u+A]=I<L?I:L,a[u+A+3]=D>W?D:W}return C}}}function xr(h,t,e,n,i,s,r){B.setBuffer(h._roots[t]),ps(0,h,e,n,i,s,r),B.clearBuffer()}function ps(h,t,e,n,i,s,r){let{float32Array:o,uint16Array:a,uint32Array:c}=B,l=h*2;if(O(l,a)){let u=J(h,c),d=K(l,a);cr(t,e,n,u,d,i,s,r)}else{let u=z(h);xt(u,o,n,s,r)&&ps(u,t,e,n,i,s,r);let d=V(h,c);xt(d,o,n,s,r)&&ps(d,t,e,n,i,s,r)}}var ll=["x","y","z"];function yr(h,t,e,n,i,s){B.setBuffer(h._roots[t]);let r=ms(0,h,e,n,i,s);return B.clearBuffer(),r}function ms(h,t,e,n,i,s){let{float32Array:r,uint16Array:o,uint32Array:a}=B,c=h*2;if(O(c,o)){let f=J(h,a),u=K(c,o);return lr(t,e,n,f,u,i,s)}else{let f=be(h,a),u=ll[f],p=n.direction[u]>=0,m,v;p?(m=z(h),v=V(h,a)):(m=V(h,a),v=z(h));let g=xt(m,r,n,i,s)?ms(m,t,e,n,i,s):null;if(g){let _=g.point[u];if(p?_<=r[v+f]:_>=r[v+f+3])return g}let x=xt(v,r,n,i,s)?ms(v,t,e,n,i,s):null;return g&&x?g.distance<=x.distance?g:x:g||x||null}}var qn=new Y,Ce=new et,Re=new et,en=new q,vr=new Z,Yn=new Z;function Mr(h,t,e,n){B.setBuffer(h._roots[t]);let i=gs(0,h,e,n);return B.clearBuffer(),i}function gs(h,t,e,n,i=null){let{float32Array:s,uint16Array:r,uint32Array:o}=B,a=h*2;if(i===null&&(e.boundingBox||e.computeBoundingBox(),vr.set(e.boundingBox.min,e.boundingBox.max,n),i=vr),O(a,r)){let l=t.geometry,f=l.index,u=l.attributes.position,d=e.index,p=e.attributes.position,m=J(h,o),v=K(a,r);if(en.copy(n).invert(),e.boundsTree)return H(h,s,Yn),Yn.matrix.copy(en),Yn.needsUpdate=!0,e.boundsTree.shapecast({intersectsBounds:g=>Yn.intersectsBox(g),intersectsTriangle:g=>{g.a.applyMatrix4(n),g.b.applyMatrix4(n),g.c.applyMatrix4(n),g.needsUpdate=!0;for(let M=m,x=v+m;M<x;M++)if(k(Re,3*t.resolveTriangleIndex(M),f,u),Re.needsUpdate=!0,g.intersectsTriangle(Re))return!0;return!1}});{let y=Wt(e);for(let g=m,M=v+m;g<M;g++){let x=t.resolveTriangleIndex(g);k(Ce,3*x,f,u),Ce.a.applyMatrix4(en),Ce.b.applyMatrix4(en),Ce.c.applyMatrix4(en),Ce.needsUpdate=!0;for(let _=0,E=y*3;_<E;_+=3)if(k(Re,_,d,p),Re.needsUpdate=!0,Ce.intersectsTriangle(Re))return!0}}}else{let l=z(h),f=V(h,o);return H(l,s,qn),!!(i.intersectsBox(qn)&&gs(l,t,e,n,i)||(H(f,s,qn),i.intersectsBox(qn)&&gs(f,t,e,n,i)))}}var Zn=new q,_s=new Z,nn=new Z,ul=new S,hl=new S,fl=new S,dl=new S;function Sr(h,t,e,n={},i={},s=0,r=1/0){t.boundingBox||t.computeBoundingBox(),_s.set(t.boundingBox.min,t.boundingBox.max,e),_s.needsUpdate=!0;let o=h.geometry,a=o.attributes.position,c=o.index,l=t.attributes.position,f=t.index,u=at.getPrimitive(),d=at.getPrimitive(),p=ul,m=hl,v=null,y=null;i&&(v=fl,y=dl);let g=1/0,M=null,x=null;return Zn.copy(e).invert(),nn.matrix.copy(Zn),h.shapecast({boundsTraverseOrder:_=>_s.distanceToBox(_),intersectsBounds:(_,E,b)=>b<g&&b<r?(E&&(nn.min.copy(_.min),nn.max.copy(_.max),nn.needsUpdate=!0),!0):!1,intersectsRange:(_,E)=>{if(t.boundsTree){let b=t.boundsTree;return b.shapecast({boundsTraverseOrder:T=>nn.distanceToBox(T),intersectsBounds:(T,C,A)=>A<g&&A<r,intersectsRange:(T,C)=>{for(let A=T,R=T+C;A<R;A++){let w=b.resolveTriangleIndex(A);k(d,3*w,f,l),d.a.applyMatrix4(e),d.b.applyMatrix4(e),d.c.applyMatrix4(e),d.needsUpdate=!0;for(let I=_,D=_+E;I<D;I++){let L=h.resolveTriangleIndex(I);k(u,3*L,c,a),u.needsUpdate=!0;let W=u.distanceToTriangle(d,p,v);if(W<g&&(m.copy(p),y&&y.copy(v),g=W,M=I,x=A),W<s)return!0}}}})}else{let b=Wt(t);for(let T=0,C=b;T<C;T++){k(d,3*T,f,l),d.a.applyMatrix4(e),d.b.applyMatrix4(e),d.c.applyMatrix4(e),d.needsUpdate=!0;for(let A=_,R=_+E;A<R;A++){let w=h.resolveTriangleIndex(A);k(u,3*w,c,a),u.needsUpdate=!0;let I=u.distanceToTriangle(d,p,v);if(I<g&&(m.copy(p),y&&y.copy(v),g=I,M=A,x=T),I<s)return!0}}}}}),at.releasePrimitive(u),at.releasePrimitive(d),g===1/0?null:(n.point?n.point.copy(m):n.point=m.clone(),n.distance=g,n.faceIndex=M,i&&(i.point?i.point.copy(y):i.point=y.clone(),i.point.applyMatrix4(Zn),m.applyMatrix4(Zn),i.distance=m.sub(i.point).length(),i.faceIndex=x),n)}var sn=new B.constructor,Jn=new B.constructor,Xt=new Gt(()=>new Y),Ie=new Y,Pe=new Y,xs=new Y,ys=new Y,vs=!1;function br(h,t,e,n){if(vs)throw new Error("MeshBVH: Recursive calls to bvhcast not supported.");vs=!0;let i=h._roots,s=t._roots,r,o=0,a=0,c=new q().copy(e).invert();for(let l=0,f=i.length;l<f;l++){sn.setBuffer(i[l]),a=0;let u=Xt.getPrimitive();H(0,sn.float32Array,u),u.applyMatrix4(c);for(let d=0,p=s.length;d<p&&(Jn.setBuffer(s[d]),r=bt(0,0,e,c,n,o,a,0,0,u),Jn.clearBuffer(),a+=s[d].byteLength/32,!r);d++);if(Xt.releasePrimitive(u),sn.clearBuffer(),o+=i[l].byteLength/32,r)break}return vs=!1,r}function bt(h,t,e,n,i,s=0,r=0,o=0,a=0,c=null,l=!1){let f,u;l?(f=Jn,u=sn):(f=sn,u=Jn);let d=f.float32Array,p=f.uint32Array,m=f.uint16Array,v=u.float32Array,y=u.uint32Array,g=u.uint16Array,M=h*2,x=t*2,_=O(M,m),E=O(x,g),b=!1;if(E&&_)l?b=i(J(t,y),K(t*2,g),J(h,p),K(h*2,m),a,r+t/8,o,s+h/8):b=i(J(h,p),K(h*2,m),J(t,y),K(t*2,g),o,s+h/8,a,r+t/8);else if(E){let T=Xt.getPrimitive();H(t,v,T),T.applyMatrix4(e);let C=z(h),A=V(h,p);H(C,d,Ie),H(A,d,Pe);let R=T.intersectsBox(Ie),w=T.intersectsBox(Pe);b=R&&bt(t,C,n,e,i,r,s,a,o+1,T,!l)||w&&bt(t,A,n,e,i,r,s,a,o+1,T,!l),Xt.releasePrimitive(T)}else{let T=z(t),C=V(t,y);H(T,v,xs),H(C,v,ys);let A=c.intersectsBox(xs),R=c.intersectsBox(ys);if(A&&R)b=bt(h,T,e,n,i,s,r,o,a+1,c,l)||bt(h,C,e,n,i,s,r,o,a+1,c,l);else if(A)if(_)b=bt(h,T,e,n,i,s,r,o,a+1,c,l);else{let w=Xt.getPrimitive();w.copy(xs).applyMatrix4(e);let I=z(h),D=V(h,p);H(I,d,Ie),H(D,d,Pe);let L=w.intersectsBox(Ie),W=w.intersectsBox(Pe);b=L&&bt(T,I,n,e,i,r,s,a,o+1,w,!l)||W&&bt(T,D,n,e,i,r,s,a,o+1,w,!l),Xt.releasePrimitive(w)}else if(R)if(_)b=bt(h,C,e,n,i,s,r,o,a+1,c,l);else{let w=Xt.getPrimitive();w.copy(ys).applyMatrix4(e);let I=z(h),D=V(h,p);H(I,d,Ie),H(D,d,Pe);let L=w.intersectsBox(Ie),W=w.intersectsBox(Pe);b=L&&bt(C,I,n,e,i,r,s,a,o+1,w,!l)||W&&bt(C,D,n,e,i,r,s,a,o+1,w,!l),Xt.releasePrimitive(w)}}return b}function Ms(h,t,e){return h===null?null:(h.point.applyMatrix4(t.matrixWorld),h.distance=h.point.distanceTo(e.ray.origin),h.object=t,h)}function Tr(){return typeof SharedArrayBuffer<"u"}function $n(h,t,e,n,i){let s=1/0,r=1/0,o=1/0,a=-1/0,c=-1/0,l=-1/0,f=1/0,u=1/0,d=1/0,p=-1/0,m=-1/0,v=-1/0,y=h.offset||0;for(let g=(t-y)*6,M=(t+e-y)*6;g<M;g+=6){let x=h[g+0],_=h[g+1],E=x-_,b=x+_;E<s&&(s=E),b>a&&(a=b),x<f&&(f=x),x>p&&(p=x);let T=h[g+2],C=h[g+3],A=T-C,R=T+C;A<r&&(r=A),R>c&&(c=R),T<u&&(u=T),T>m&&(m=T);let w=h[g+4],I=h[g+5],D=w-I,L=w+I;D<o&&(o=D),L>l&&(l=L),w<d&&(d=w),w>v&&(v=w)}n[0]=s,n[1]=r,n[2]=o,n[3]=a,n[4]=c,n[5]=l,i[0]=f,i[1]=u,i[2]=d,i[3]=p,i[4]=m,i[5]=v}var Lt=32,ml=(h,t)=>h.candidate-t.candidate,qt=new Array(Lt).fill().map(()=>({count:0,bounds:new Float32Array(6),rightCacheBounds:new Float32Array(6),leftCacheBounds:new Float32Array(6),candidate:0})),Kn=new Float32Array(6);function Ar(h,t,e,n,i,s){let r=-1,o=0;if(s===0)r=as(t),r!==-1&&(o=(t[r]+t[r+3])/2);else if(s===1)r=as(h),r!==-1&&(o=gl(e,n,i,r));else if(s===2){let a=Ee(h),c=1.25*i,l=e.offset||0,f=(n-l)*6,u=(n+i-l)*6;for(let d=0;d<3;d++){let p=t[d],y=(t[d+3]-p)/Lt;if(i<Lt/4){let g=[...qt];g.length=i;let M=0;for(let _=f;_<u;_+=6,M++){let E=g[M];E.candidate=e[_+2*d],E.count=0;let{bounds:b,leftCacheBounds:T,rightCacheBounds:C}=E;for(let A=0;A<3;A++)C[A]=1/0,C[A+3]=-1/0,T[A]=1/0,T[A+3]=-1/0,b[A]=1/0,b[A+3]=-1/0;Ke(_,e,b)}g.sort(ml);let x=i;for(let _=0;_<x;_++){let E=g[_];for(;_+1<x&&g[_+1].candidate===E.candidate;)g.splice(_+1,1),x--}for(let _=f;_<u;_+=6){let E=e[_+2*d];for(let b=0;b<x;b++){let T=g[b];E>=T.candidate?Ke(_,e,T.rightCacheBounds):(Ke(_,e,T.leftCacheBounds),T.count++)}}for(let _=0;_<x;_++){let E=g[_],b=E.count,T=i-E.count,C=E.leftCacheBounds,A=E.rightCacheBounds,R=0;b!==0&&(R=Ee(C)/a);let w=0;T!==0&&(w=Ee(A)/a);let I=1+1.25*(R*b+w*T);I<c&&(r=d,c=I,o=E.candidate)}}else{for(let x=0;x<Lt;x++){let _=qt[x];_.count=0,_.candidate=p+y+x*y;let E=_.bounds;for(let b=0;b<3;b++)E[b]=1/0,E[b+3]=-1/0}for(let x=f;x<u;x+=6){let b=~~((e[x+2*d]-p)/y);b>=Lt&&(b=Lt-1);let T=qt[b];T.count++,Ke(x,e,T.bounds)}let g=qt[Lt-1];cs(g.bounds,g.rightCacheBounds);for(let x=Lt-2;x>=0;x--){let _=qt[x],E=qt[x+1];ls(_.bounds,E.rightCacheBounds,_.rightCacheBounds)}let M=0;for(let x=0;x<Lt-1;x++){let _=qt[x],E=_.count,b=_.bounds,C=qt[x+1].rightCacheBounds;E!==0&&(M===0?cs(b,Kn):ls(b,Kn,Kn)),M+=E;let A=0,R=0;M!==0&&(A=Ee(Kn)/a);let w=i-M;w!==0&&(R=Ee(C)/a);let I=1+1.25*(A*M+R*w);I<c&&(r=d,c=I,o=_.candidate)}}}}else console.warn(`BVH: Invalid build strategy value ${s} used.`);return{axis:r,pos:o}}function gl(h,t,e,n){let i=0,s=h.offset;for(let r=t,o=t+e;r<o;r++)i+=h[(r-s)*6+n*2];return i/e}var De=class{constructor(){this.boundingData=new Float32Array(6)}};function wr(h,t,e,n,i,s){let r=n,o=n+i-1,a=s.pos,c=s.axis*2,l=e.offset||0;for(;;){for(;r<=o&&e[(r-l)*6+c]<a;)r++;for(;r<=o&&e[(o-l)*6+c]>=a;)o--;if(r<o){for(let f=0;f<t;f++){let u=h[r*t+f];h[r*t+f]=h[o*t+f],h[o*t+f]=u}for(let f=0;f<6;f++){let u=r-l,d=o-l,p=e[u*6+f];e[u*6+f]=e[d*6+f],e[d*6+f]=p}r++,o--}else return r}}var Cr,Qn,Ss,Rr,_l=Math.pow(2,32);function jn(h){return"count"in h?1:1+jn(h.left)+jn(h.right)}function Ir(h,t,e){return Cr=new Float32Array(e),Qn=new Uint32Array(e),Ss=new Uint16Array(e),Rr=new Uint8Array(e),bs(h,t)}function bs(h,t){let e=h/4,n=h/2,i="count"in t,s=t.boundingData;for(let r=0;r<6;r++)Cr[e+r]=s[r];if(i)return t.buffer?(Rr.set(new Uint8Array(t.buffer),h),h+t.buffer.byteLength):(Qn[e+6]=t.offset,Ss[n+14]=t.count,Ss[n+15]=65535,h+32);{let{left:r,right:o,splitAxis:a}=t,c=h+32,l=bs(c,r),f=h/32,d=l/32-f;if(d>_l)throw new Error("MeshBVH: Cannot store relative child node offset greater than 32 bits.");return Qn[e+6]=d,Qn[e+7]=a,bs(l,o)}}function xl(h,t,e,n,i){let{maxDepth:s,verbose:r,maxLeafSize:o,strategy:a,onProgress:c}=i,l=h.primitiveBuffer,f=h.primitiveBufferStride,u=new Float32Array(6),d=!1,p=new De;return $n(t,e,n,p.boundingData,u),v(p,e,n,u),p;function m(y){c&&c(y/n)}function v(y,g,M,x=null,_=0){if(!d&&_>=s&&(d=!0,r&&console.warn(`BVH: Max depth of ${s} reached when generating BVH. Consider increasing maxDepth.`)),M<=o||_>=s)return m(g+M),y.offset=g,y.count=M,y;let E=Ar(y.boundingData,x,t,g,M,a);if(E.axis===-1)return m(g+M),y.offset=g,y.count=M,y;let b=wr(l,f,t,g,M,E);if(b===g||b===g+M)m(g+M),y.offset=g,y.count=M;else{y.splitAxis=E.axis;let T=new De,C=g,A=b-g;y.left=T,$n(t,C,A,T.boundingData,u),v(T,C,A,u,_+1);let R=new De,w=b,I=M-A;y.right=R,$n(t,w,I,R.boundingData,u),v(R,w,I,u,_+1)}return y}}function Pr(h,t){let e=t.useSharedArrayBuffer?SharedArrayBuffer:ArrayBuffer,n=h.getRootRanges(t.range),i=n[0],s=n[n.length-1],r={offset:i.offset,count:s.offset+s.count-i.offset},o=new Float32Array(6*r.count);o.offset=r.offset,h.computePrimitiveBounds(r.offset,r.count,o),h._roots=n.map(a=>{let c=xl(h,o,a.offset,a.count,t),l=jn(c),f=new e(32*l);return Ir(0,c,f),f})}var Yt,Ue,Le=[],ti=new Gt(()=>new Y);function Dr(h,t,e,n,i,s){Yt=ti.getPrimitive(),Ue=ti.getPrimitive(),Le.push(Yt,Ue),B.setBuffer(h._roots[t]);let r=Ts(0,h.geometry,e,n,i,s);B.clearBuffer(),ti.releasePrimitive(Yt),ti.releasePrimitive(Ue),Le.pop(),Le.pop();let o=Le.length;return o>0&&(Ue=Le[o-1],Yt=Le[o-2]),r}function Ts(h,t,e,n,i=null,s=0,r=0){let{float32Array:o,uint16Array:a,uint32Array:c}=B,l=h*2;if(O(l,a)){let u=J(h,c),d=K(l,a);return H(h,o,Yt),n(u,d,!1,r,s+h/8,Yt)}else{let A=function(w){let{uint16Array:I,uint32Array:D}=B,L=w*2;for(;!O(L,I);)w=z(w),L=w*2;return J(w,D)},R=function(w){let{uint16Array:I,uint32Array:D}=B,L=w*2;for(;!O(L,I);)w=V(w,D),L=w*2;return J(w,D)+K(L,I)},u=z(h),d=V(h,c),p=u,m=d,v,y,g,M;if(i&&(g=Yt,M=Ue,H(p,o,g),H(m,o,M),v=i(g),y=i(M),y<v)){p=d,m=u;let w=v;v=y,y=w,g=M}g||(g=Yt,H(p,o,g));let x=O(p*2,a),_=e(g,x,v,r+1,s+p/8),E;if(_===2){let w=A(p),D=R(p)-w;E=n(w,D,!0,r+1,s+p/8,g)}else E=_&&Ts(p,t,e,n,i,s,r+1);if(E)return!0;M=Ue,H(m,o,M);let b=O(m*2,a),T=e(M,b,y,r+1,s+m/8),C;if(T===2){let w=A(m),D=R(m)-w;C=n(w,D,!0,r+1,s+m/8,M)}else C=T&&Ts(m,t,e,n,i,s,r+1);return!!C}}var Lr=new Y,ei=class{constructor(){this._roots=null,this.primitiveBuffer=null,this.primitiveBufferStride=null}init(t){t={...On,...t},Pr(this,t)}getRootRanges(t){return Qe(this.geometry,t,this.primitiveStride)}raycastObject3D(){throw new Error("BVH: raycastObject3D() not implemented")}shiftPrimitiveOffsets(t){let e=this._indirectBuffer;if(e)for(let n=0,i=e.length;n<i;n++)e[n]+=t;else{let n=this._roots;for(let i=0;i<n.length;i++){let s=n[i],r=new Uint32Array(s),o=new Uint16Array(s),a=s.byteLength/32;for(let c=0;c<a;c++){let l=8*c,f=2*l;O(f,o)&&(r[l+6]+=t)}}}}traverse(t,e=0){let n=this._roots[e],i=new Uint32Array(n),s=new Uint16Array(n);r(0);function r(o,a=0){let c=o*2,l=O(c,s);if(l){let f=i[o+6],u=s[c+14];t(a,l,new Float32Array(n,o*4,6),f,u)}else{let f=z(o),u=V(o,i),d=be(o,i);t(a,l,new Float32Array(n,o*4,6),d)||(r(f,a+1),r(u,a+1))}}}getBoundingBox(t){return t.makeEmpty(),this._roots.forEach(n=>{H(0,new Float32Array(n),Lr),t.union(Lr)}),t}shapecast(t){let{boundsTraverseOrder:e,intersectsBounds:n,intersectsRange:i,intersectsPrimitive:s,scratchPrimitive:r,iterate:o}=t;if(i&&s){let f=i;i=(u,d,p,m,v)=>f(u,d,p,m,v)?!0:o(u,d,this,s,p,m,r)}else i||(s?i=(f,u,d,p)=>o(f,u,this,s,d,p,r):i=(f,u,d)=>d);let a=!1,c=0,l=this._roots;for(let f=0,u=l.length;f<u;f++){let d=l[f];if(a=Dr(this,f,n,i,e,c),a)break;c+=d.byteLength/32}return a}};function vl(h,t){let e=h[h.length-1],n=e.offset+e.count>2**16,i=h.reduce((c,l)=>c+l.count,0),s=n?4:2,r=t?new SharedArrayBuffer(i*s):new ArrayBuffer(i*s),o=n?new Uint32Array(r):new Uint16Array(r),a=0;for(let c=0;c<h.length;c++){let{offset:l,count:f}=h[c];for(let u=0;u<f;u++)o[a+u]=l+u;a+=f}return o}var ni=class extends ei{get indirect(){return!!this._indirectBuffer}get primitiveStride(){return null}get primitiveBufferStride(){return this.indirect?1:this.primitiveStride}set primitiveBufferStride(t){}get primitiveBuffer(){return this.indirect?this._indirectBuffer:this.geometry.index.array}set primitiveBuffer(t){}constructor(t,e={}){if(t.isBufferGeometry){if(t.index&&t.index.isInterleavedBufferAttribute)throw new Error("BVH: InterleavedBufferAttribute is not supported for the index attribute.")}else throw new Error("BVH: Only BufferGeometries are supported.");if(e.useSharedArrayBuffer&&!Tr())throw new Error("BVH: SharedArrayBuffer is not available.");super(),this.geometry=t,this.resolvePrimitiveIndex=e.indirect?n=>this._indirectBuffer[n]:n=>n,this.primitiveBuffer=null,this.primitiveBufferStride=null,this._indirectBuffer=null,e={...On,...e},e[Ye]||this.init(e)}init(t){let{geometry:e,primitiveStride:n}=this;if(t.indirect){let i=Qe(e,t.range,n),s=vl(i,t.useSharedArrayBuffer);this._indirectBuffer=s}else dr(e,t);super.init(t),!e.boundingBox&&t.setBoundingBox&&(e.boundingBox=this.getBoundingBox(new Y))}computePrimitiveBounds(){throw new Error("BVH: computePrimitiveBounds() not implemented")}getRootRanges(t){return this.indirect?[{offset:0,count:this._indirectBuffer.length}]:Qe(this.geometry,t,this.primitiveStride)}raycastObject3D(){throw new Error("BVH: raycastObject3D() not implemented")}shapecast(t){let{iterateDirect:e,iterateIndirect:n,...i}=t,s=this.indirect?n:e;return super.shapecast({...i,iterate:s})}};var ii=new Z,si=new Ge,Ur=new S,Nr=new q,Fr=new S,rn=class h extends ni{static serialize(t,e={}){e={cloneBuffers:!0,...e};let n=t.geometry,i=t._roots,s=t._indirectBuffer,r=n.getIndex(),o={version:1,roots:null,index:null,indirectBuffer:null};return e.cloneBuffers?(o.roots=i.map(a=>a.slice()),o.index=r?r.array.slice():null,o.indirectBuffer=s?s.slice():null):(o.roots=i,o.index=r?r.array:null,o.indirectBuffer=s),o}static deserialize(t,e,n={}){n={setIndex:!0,indirect:!!t.indirectBuffer,...n};let{index:i,roots:s,indirectBuffer:r}=t;t.version||(console.warn("MeshBVH.deserialize: Serialization format has been changed and will be fixed up. It is recommended to regenerate any stored serialized data."),a(s));let o=new h(e,{...n,[Ye]:!0});if(o._roots=s,o._indirectBuffer=r||null,n.setIndex){let c=e.getIndex();if(c===null){let l=new st(t.index,1,!1);e.setIndex(l)}else c.array!==i&&(c.array.set(i),c.needsUpdate=!0)}return o;function a(c){for(let l=0;l<c.length;l++){let f=c[l],u=new Uint32Array(f),d=new Uint16Array(f);for(let p=0,m=f.byteLength/32;p<m;p++){let v=8*p,y=2*v;O(y,d)||(u[v+6]=u[v+6]/8-p)}}}}get primitiveStride(){return 3}get resolveTriangleIndex(){return this.resolvePrimitiveIndex}constructor(t,e={}){e.maxLeafTris&&(e={...e,maxLeafSize:e.maxLeafTris}),super(t,e)}shiftTriangleOffsets(t){return super.shiftPrimitiveOffsets(t)}computePrimitiveBounds(t,e,n){let i=this.geometry,s=this._indirectBuffer,r=i.attributes.position,o=i.index?i.index.array:null,a=r.normalized;if(t<0||e+t-n.offset>n.length/6)throw new Error("MeshBVH: compute triangle bounds range is invalid.");let c=r.array,l=r.offset||0,f=3;r.isInterleavedBufferAttribute&&(f=r.data.stride);let u=["getX","getY","getZ"],d=n.offset;for(let p=t,m=t+e;p<m;p++){let y=(s?s[p]:p)*3,g=(p-d)*6,M=y+0,x=y+1,_=y+2;o&&(M=o[M],x=o[x],_=o[_]),a||(M=M*f+l,x=x*f+l,_=_*f+l);for(let E=0;E<3;E++){let b,T,C;a?(b=r[u[E]](M),T=r[u[E]](x),C=r[u[E]](_)):(b=c[M+E],T=c[x+E],C=c[_+E]);let A=b;T<A&&(A=T),C<A&&(A=C);let R=b;T>R&&(R=T),C>R&&(R=C);let w=(R-A)/2,I=E*2;n[g+I+0]=A+w,n[g+I+1]=w+(Math.abs(A)+w)*Js}}return n}raycastObject3D(t,e,n=[]){let{material:i}=t;if(i===void 0)return;Nr.copy(t.matrixWorld).invert(),si.copy(e.ray).applyMatrix4(Nr),Fr.setFromMatrixScale(t.matrixWorld),Ur.copy(si.direction).multiply(Fr);let s=Ur.length(),r=e.near/s,o=e.far/s;if(e.firstHitOnly===!0){let a=this.raycastFirst(si,i,r,o);a=Ms(a,t,e),a&&n.push(a)}else{let a=this.raycast(si,i,r,o);for(let c=0,l=a.length;c<l;c++){let f=Ms(a[c],t,e);f&&n.push(f)}}return n}refit(t=null){return(this.indirect?_r:ar)(this,t)}raycast(t,e=Fn,n=0,i=1/0){let s=this._roots,r=[],o=this.indirect?xr:hr;for(let a=0,c=s.length;a<c;a++)o(this,a,e,t,r,n,i);return r}raycastFirst(t,e=Fn,n=0,i=1/0){let s=this._roots,r=null,o=this.indirect?yr:fr;for(let a=0,c=s.length;a<c;a++){let l=o(this,a,e,t,n,i);l!=null&&(r==null||l.distance<r.distance)&&(r=l)}return r}intersectsGeometry(t,e){let n=!1,i=this._roots,s=this.indirect?Mr:mr;for(let r=0,o=i.length;r<o&&(n=s(this,r,t,e),!n);r++);return n}shapecast(t){let e=at.getPrimitive(),n=super.shapecast({...t,intersectsPrimitive:t.intersectsTriangle,scratchPrimitive:e,iterateDirect:or,iterateIndirect:ur});return at.releasePrimitive(e),n}bvhcast(t,e,n){let{intersectsRanges:i,intersectsTriangles:s}=n,r=at.getPrimitive(),o=this.geometry.index,a=this.geometry.attributes.position,c=this.indirect?p=>{let m=this.resolveTriangleIndex(p);k(r,m*3,o,a)}:p=>{k(r,p*3,o,a)},l=at.getPrimitive(),f=t.geometry.index,u=t.geometry.attributes.position,d=t.indirect?p=>{let m=t.resolveTriangleIndex(p);k(l,m*3,f,u)}:p=>{k(l,p*3,f,u)};if(s){let p=(m,v,y,g,M,x,_,E)=>{for(let b=y,T=y+g;b<T;b++){d(b),l.a.applyMatrix4(e),l.b.applyMatrix4(e),l.c.applyMatrix4(e),l.needsUpdate=!0;for(let C=m,A=m+v;C<A;C++)if(c(C),r.needsUpdate=!0,s(r,l,C,b,M,x,_,E))return!0}return!1};if(i){let m=i;i=function(v,y,g,M,x,_,E,b){return m(v,y,g,M,x,_,E,b)?!0:p(v,y,g,M,x,_,E,b)}}else i=p}return br(this,t,e,i)}intersectsBox(t,e){return ii.set(t.min,t.max,e),ii.needsUpdate=!0,this.shapecast({intersectsBounds:n=>ii.intersectsBox(n),intersectsTriangle:n=>ii.intersectsTriangle(n)})}intersectsSphere(t){return this.shapecast({intersectsBounds:e=>t.intersectsBox(e),intersectsTriangle:e=>e.intersectsSphere(t)})}closestPointToGeometry(t,e,n={},i={},s=0,r=1/0){return(this.indirect?Sr:gr)(this,t,e,n,i,s,r)}closestPointToPoint(t,e={},n=0,i=1/0){return Qs(this,t,e,n,i)}};self.onmessage=({data:h})=>{let t=performance.now();function e(r){r=Math.min(r,1);let o=performance.now();o-t>=10&&r!==1&&(self.postMessage({error:null,serialized:null,position:null,progress:r}),t=o)}let{index:n,position:i,options:s}=h;try{let r=new Xe;if(r.setAttribute("position",new st(i,3,!1)),n&&r.setIndex(new st(n,1,!1)),s.includedProgressCallback&&(s.onProgress=e),s.groups){let l=s.groups;for(let f in l){let u=l[f];r.addGroup(u.start,u.count,u.materialIndex)}}let o=new rn(r,s),a=rn.serialize(o,{copyIndexBuffer:!1}),c=[i.buffer,...a.roots];a.index&&c.push(a.index.buffer),c=c.filter(l=>typeof SharedArrayBuffer>"u"||!(l instanceof SharedArrayBuffer)),o._indirectBuffer&&c.push(a.indirectBuffer.buffer),self.postMessage({error:null,serialized:a,position:i,progress:1},c)}catch(r){self.postMessage({error:r,serialized:null,position:null,progress:1})}};
/*! Bundled license information:

three/build/three.core.js:
three/build/three.module.js:
  (**
   * @license
   * Copyright 2010-2025 Three.js Authors
   * SPDX-License-Identifier: MIT
   *)
*/
