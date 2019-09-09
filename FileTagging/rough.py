from datetime import datetime
import re

start = datetime.now()

stop_words = ['A', 'About', 'Above', 'Above', 'Across', 'After', 'Afterwards', 'Again', 'Against', 'All', 'Almost', 'Alone', 'Along', 'Already',
              'Also', 'Although', 'Always', 'Am', 'Among', 'Amongst', 'Amoungst', 'Amount', 'An', 'And', 'Another', 'Any', 'Anyhow', 'Anyone',
              'Anything', 'Anyway', 'Anywhere', 'Are', 'Around', 'As', 'At', 'Back', 'Be', 'Became', 'Because', 'Become', 'Becomes', 'Becoming',
              'Been', 'Before', 'Beforehand', 'Behind', 'Being', 'Below', 'Beside', 'Besides', 'Between', 'Beyond', 'Bill', 'Both', 'Bottom',
              'But', 'By', 'Call', 'Can', 'Cannot', 'Cant', 'Co', 'Con', 'Could', 'Couldnt', 'Cry', 'De', 'Describe', 'Detail', 'Do', 'Done',
              'Down', 'Due', 'During', 'Each', 'Eg', 'Eight', 'Either', 'Eleven', 'Else', 'Elsewhere', 'Empty', 'Enough', 'Etc', 'Even', 'Ever',
              'Every', 'Everyone', 'Everything', 'Everywhere', 'Except', 'Few', 'Fifteen', 'Fify', 'Fill', 'Find', 'Fire', 'First', 'Five', 'For',
              'Former', 'Formerly', 'Forty', 'Found', 'Four', 'From', 'Front', 'Full', 'Further', 'Get', 'Give', 'Go', 'Had', 'Has', 'Hasnt',
              'Have', 'He', 'Hence', 'Her', 'Here', 'Hereafter', 'Hereby', 'Herein', 'Hereupon', 'Hers', 'Herself', 'Him', 'Himself', 'His',
              'How', 'However', 'Hundred', 'Ie', 'If', 'In', 'Inc', 'Indeed', 'Interest', 'Into', 'Is', 'It', 'Its', 'Itself', 'Keep', 'Last',
              'Latter', 'Latterly', 'Least', 'Less', 'Ltd', 'Made', 'Many', 'May', 'Me', 'Meanwhile', 'Might', 'Mill', 'Mine', 'More', 'Moreover',
              'Most', 'Mostly', 'Move', 'Much', 'Must', 'My', 'Myself', 'Name', 'Namely', 'Neither', 'Never', 'Nevertheless', 'Next', 'Nine', 'No',
              'Nobody', 'None', 'Noone', 'Nor', 'Not', 'Nothing', 'Now', 'Nowhere', 'Of', 'Off', 'Often', 'On', 'Once', 'One', 'Only', 'Onto', 'Or',
              'Other', 'Others', 'Otherwise', 'Our', 'Ours', 'Ourselves', 'Out', 'Over', 'Own', 'Part', 'Per', 'Perhaps', 'Please', 'Put', 'Rather',
              'Re', 'Same', 'See', 'Seem', 'Seemed', 'Seeming', 'Seems', 'Serious', 'Several', 'She', 'Should', 'Show', 'Side', 'Since', 'Sincere',
              'Six', 'Sixty', 'So', 'Some', 'Somehow', 'Someone', 'Something', 'Sometime', 'Sometimes', 'Somewhere', 'Still', 'Such', 'System', 'Take',
              'Ten', 'Than', 'That', 'The', 'Their', 'Them', 'Themselves', 'Then', 'Thence', 'There', 'Thereafter', 'Thereby', 'Therefore', 'Therein',
              'Thereupon', 'These', 'They', 'Thick', 'Thin', 'Third', 'This', 'Those', 'Though', 'Three', 'Through', 'Throughout', 'Thru', 'Thus', 'To',
              'Together', 'Too', 'Top', 'Toward', 'Towards', 'Twelve', 'Twenty', 'Two', 'Un', 'Under', 'Until', 'Up', 'Upon', 'Us', 'Very', 'Via', 'Was',
              'We', 'Well', 'Were', 'What', 'Whatever', 'When', 'Whence', 'Whenever', 'Where', 'Whereafter', 'Whereas', 'Whereby', 'Wherein', 'Whereupon',
              'Wherever', 'Whether', 'Which', 'While', 'Whither', 'Who', 'Whoever', 'Whole', 'Whom', 'Whose', 'Why', 'Will', 'With', 'Within', 'Without',
              'Would', 'Yet', 'You', 'Your', 'Yours', 'Yourself', 'Yourselves', 'The', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
              'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

str_list = ["New Bank", "Bank of America", "Bank of Newyork", "Bank at Europe", "Old Bank of America", "Old Church of South",
            'Winston & Strawn', 'Winston & Strawn L.L.P.', 'Winston Mills, Inc', 'Winston N K Corp', 'Winston N K Corporation',
            'Winston Network Inc', 'Winston Network Inc.', 'The Nixon Law Firm', 'The Rosen Law Firm', 'The Rosen Law Firm P.A.',
            'The Alexander Firm', 'The Alexander Firm P.C.', 'The Kane Capital Firm Pc', 'The Amlong', 'The Ashcroft Law Firm',
            'The Ashcroft Law Firm L.L.C.', 'The Berry Firm', "D Young man Valley", "D Young the Valley",
            "F Young man in the Valley"]

keyword_list = ["Bank of America", "Winston & Strawn LLP", "New Church", "New Playground of India", "Old Church of South",
                "new", "Bank of (America) is the", "Bank at new", "This is a Kane Capital Investment Group LLC", "D Young man in the Valley",
                "F a R Young man in the Valley"]

for keyword in keyword_list:
    if '(' in keyword:
        keyword_para = keyword.split('(')
        keyword = keyword_para[0]
    key_list = keyword.split(' ')
    if len(key_list) > 1:
        new_key_list = []
        stop_word_key = []
        for i in range(len(key_list) - 1):
            if new_key_list:
                new_key_list.append(new_key_list[-1] + " " + key_list[i])
            else:
                if key_list[i].title() in stop_words:
                    stop_word_key.append(key_list[i])
                else:
                    if stop_word_key:
                        new_key = str(' '.join(stop_word_key))
                        new_key = new_key + ' ' + key_list[i]
                        print(new_key)
                        new_key_list.append(new_key)
                    else:
                        new_key_list.append(key_list[i])

    else:
        new_key_list = key_list

    match_found = []
    temp_list = []
    for i in range(len(new_key_list)):
        if i < 1:
            for sentence in str_list:
                search_key = r'^{}\s'.format(new_key_list[i])
                match = re.search(search_key, sentence)
                if match:
                    match_found.append(sentence)

        else:
            for sentence in match_found:
                search_key = r'^{}\s'.format(new_key_list[i])
                match = re.search(search_key, sentence)
                if match:
                    temp_list.append(sentence)

            if not temp_list:
                break

        if temp_list:
            match_found.clear()
            match_found = temp_list.copy()
            temp_list.clear()

    print(match_found)

    # for sentence in str_list:
    #     new_key = new_key_list[-1]
    #     new_key = str(new_key)
    #     search_key = r'^{}\s'.format(new_key)
    #     match = re.search(search_key, sentence)
    #     if match:
    #     # if sentence.startswith(new_key_list[-1]):
    #         print(str_list.index(sentence))
    #         print(new_key_list[-1])

    # for key in new_key_list:
    #     for sentence in str_list:
    #         if sentence.startswith(key):
    #             if key == new_key_list[-1]:
    #                 print(str_list.index(sentence))
    #                 print(key)
    #         else:
    #             break


end = datetime.now()
print(end - start)
