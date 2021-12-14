from collections import defaultdict

def parse(diff_output):
    if not isinstance(diff_output, str) or not diff_output:
        return set()
    diff_output = '\n'.join([line for line in diff_output.strip().split('\n') if line])
    return Parser().parse_changed_lines_lut(diff_output)

class Parser:

    def parse_changed_lines_dict(self, diff_output):
        output = diff_output
        changed_files_with_lines = self.parse(output)
        res = defaultdict(list)
        for filename, lines in changed_files_with_lines:
            res[filename] += lines
        return dict(res)

    def parse_changed_lines_lut(self, diff_output):
        res = set()
        for filename, lines in self.parse_changed_lines_dict(diff_output).items():
            for line in lines:
                res.add((filename, line))
        return res


    def parse(self, diff_output):
        blocks = diff_output.split('diff --git a/')
        files = [self._parse_block(b) for b in blocks]
        return [f for f in files if f]

    def _parse_block(self, block):
        lines = block.split('\n')
        parts = lines[0].split(' b/')
        if len(parts) != 2:
            return None
        path, _ = parts
        
        line_numbers = set()
        for line in lines:
            line_numbers.update(self._parse_range(line))

        return (
            path,
            sorted(line_numbers)
        )

    def _parse_range(self, line):
        parts = line.split('@@')

        if len(parts) != 3:
            return []
        
        _, ranges_str, _ = parts
        ranges = [self._parse_range_str(r) for r in ranges_str.split(' ') if r]
        res = set()
        for r in ranges:
            res.update(r)
        return sorted(res)

    def _parse_range_str(self, range_str):
        try:
            start, count = [abs(int(p)) for p in range_str.split(',')]
            return list(range(start, start+count)) 
        except:
            return []
        

